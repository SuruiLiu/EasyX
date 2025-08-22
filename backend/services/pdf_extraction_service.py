import pdfplumber
import re
import io
from typing import Dict, Any
from datetime import datetime
from models.pdf_extraction_types import META_JSON_EXAMPLE

class PdfExtractionService:
    """Service for extracting data from PDF timesheet files"""

    def extract_timesheet_data(self, pdf_file_stream) -> Dict[str, Any]:
        """
        Extracts timesheet data from a PDF file stream.
        Returns structured JSON data based on the timesheet format.
        """
        try:
            with pdfplumber.open(pdf_file_stream) as pdf:
                page = pdf.pages[0]  # Assuming timesheet is on first page
                text = page.extract_text()
                tables = page.extract_tables()
                
                # Extract data based on the timesheet structure
                extracted_data = {
                    "timesheet_info": {
                        "employee_name": self._extract_employee_name(tables),
                        "week_worked": self._extract_week_worked(text),
                        "status": "Processed"
                    },
                    "email_particulars": {
                        "expected_email_address": self._extract_email_address(text),
                        "expected_email_subject": self._extract_email_subject(text),
                        "no_additional_attachments": True,
                        "date_received_email_link": self._extract_date_received(text)
                    },
                    "contract_particulars": self._extract_contract_particulars(tables),
                    "extracted_table_data": self._extract_table_data(tables, text)
                }
                
                return extracted_data
                
        except Exception as e:
            print(f"Error during PDF extraction: {e}")
            return {"error": str(e)}

    def extractMeta(self, pdf_file_stream) -> Dict[str, Any]:
        """
        Extract structured meta data from PDF file stream.
        Returns the complete meta JSON structure.
        """
        try:
            with pdfplumber.open(pdf_file_stream) as pdf:
                page = pdf.pages[0]
                text = page.extract_text()
                tables = page.extract_tables()
                
                if not tables or len(tables) < 4:
                    return {"error": "Invalid PDF structure - expected 4 tables"}
                
                # Extract base information from table 1
                base_info = self._extract_base_info(tables[0])
                
                # Extract employee information from table 2
                employee_info = self._extract_employee_info(tables[1])
                
                # Extract work entries from table 3
                work_entries = self._extract_work_entries(tables[2])
                
                # Extract tasks and totals from table 4
                tasks, totals_row, weekly_total = self._extract_tasks_and_totals(tables[3])
                
                # Extract date from text
                date = self._extract_date(text)
                
                # Build the complete meta structure
                meta_data = {
                    "base": base_info,
                    "employee": employee_info,
                    "work_entries": work_entries,
                    "weekly_total": weekly_total,
                    "tasks": tasks,
                    "totals_row": totals_row,
                    "date": date
                }
                
                return meta_data
                
        except Exception as e:
            print(f"Error during meta extraction: {e}")
            return {"error": str(e)}

    def get_pdf_text(self, pdf_file_stream) -> str:
        """Extracts all text from PDF for preview purposes"""
        try:
            with pdfplumber.open(pdf_file_stream) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            return f"Error extracting text: {e}"

    def _extract_base_info(self, table) -> Dict[str, str]:
        """Extract base information from table 1"""
        base_info = {
            "po_number": "Unknown",
            "client": "Unknown",
            "supervisor": "Unknown"
        }
        
        for row in table:
            if row and len(row) >= 2:
                key = str(row[0]).lower().strip()
                value = str(row[1]).strip()
                
                if 'po number' in key:
                    base_info["po_number"] = value
                elif 'client' in key:
                    base_info["client"] = value
                elif 'supervisor' in key:
                    base_info["supervisor"] = value
        
        return base_info

    def _extract_employee_info(self, table) -> Dict[str, str]:
        """Extract employee information from table 2"""
        employee_info = {
            "name": "Unknown",
            "company": "Unknown"
        }
        
        for row in table:
            if row and len(row) >= 2:
                key = str(row[0]).lower().strip()
                value = str(row[1]).strip()
                
                if 'name' in key:
                    employee_info["name"] = value
                elif 'company' in key:
                    employee_info["company"] = value
        
        return employee_info

    def _extract_work_entries(self, table) -> list:
        """Extract work entries from table 3"""
        work_entries = []
        
        # Skip header rows
        data_rows = []
        for row in table:
            if row and len(row) >= 9:
                first_cell = str(row[0]).strip().lower()
                if first_cell in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                    data_rows.append(row)
        
        for row in data_rows:
            weekday = str(row[0]).strip()
            date_original = str(row[1]).strip()
            
            # Extract morning period
            morning = {
                "start": str(row[2]).strip(),
                "finish": str(row[3]).strip(),
                "time": str(row[4]).strip()
            }
            
            # Extract afternoon period
            afternoon = {
                "start": str(row[5]).strip(),
                "finish": str(row[6]).strip(),
                "time": str(row[7]).strip()
            }
            
            # Extract total daily hours
            total_daily_hours = str(row[8]).strip()
            total_daily_decimal = self._convert_time_to_decimal(total_daily_hours)
            
            # Extract extra in/out (default values)
            extra_in_out = {
                "morning": "0:00",
                "afternoon": "0:00"
            }
            
            # Convert date to ISO format
            date_iso = self._convert_date_to_iso(date_original)
            
            work_entry = {
                "weekday": weekday,
                "date_original": date_original,
                "date_iso": date_iso,
                "morning": morning,
                "afternoon": afternoon,
                "extra_in_out": extra_in_out,
                "total_daily_hours": total_daily_hours,
                "total_daily_decimal": total_daily_decimal
            }
            
            work_entries.append(work_entry)
        
        return work_entries

    def _extract_tasks_and_totals(self, table) -> tuple:
        """Extract tasks and totals from table 4"""
        tasks = []
        totals_row = {}
        weekly_total = {"total_hours": "0:00", "total_decimal_hours": 0.0}
        
        # Find the task row (usually row 1)
        task_row = None
        totals_data = {}
        
        for i, row in enumerate(table):
            if not row:
                continue
            
            first_cell = str(row[0]).strip()
            
            if first_cell == "Task1":
                task_row = row
            elif "Total Hours" in first_cell:
                # This is the totals row
                totals_data = {
                    "Mon": str(row[1]).strip() if len(row) > 1 else "0:00",
                    "Tues": str(row[2]).strip() if len(row) > 2 else "0:00",
                    "Wed": str(row[3]).strip() if len(row) > 3 else "0:00",
                    "Thur": str(row[4]).strip() if len(row) > 4 else "0:00",
                    "Fri": str(row[5]).strip() if len(row) > 5 else "0:00",
                    "Sat": str(row[6]).strip() if len(row) > 6 else "0:00",
                    "Sun": str(row[6]).strip() if len(row) > 6 else "0:00"  # Same as Sat/Sun
                }
                
                # Extract total hours
                if len(row) > 7:
                    total_hours = str(row[7]).strip()
                    total_decimal = self._convert_time_to_decimal(total_hours)
                    weekly_total = {
                        "total_hours": total_hours,
                        "total_decimal_hours": total_decimal
                    }
        
        # Build task information
        if task_row:
            task = {
                "task_name": "Task1",
                "per_day": {
                    "Mon": str(task_row[1]).strip() if len(task_row) > 1 else "0:00",
                    "Tues": str(task_row[2]).strip() if len(task_row) > 2 else "0:00",
                    "Wed": str(task_row[3]).strip() if len(task_row) > 3 else "0:00",
                    "Thur": str(task_row[4]).strip() if len(task_row) > 4 else "0:00",
                    "Fri": str(task_row[5]).strip() if len(task_row) > 5 else "0:00",
                    "Sat/Sun": str(task_row[6]).strip() if len(task_row) > 6 else "0:00"
                },
                "total_hours": weekly_total["total_hours"],
                "decimal_hours": weekly_total["total_decimal_hours"]
            }
            tasks.append(task)
        
        # Build totals row
        totals_row = {
            "label": "Total Hours",
            "by_day": totals_data,
            "total_hours": weekly_total["total_hours"],
            "total_decimal_hours": weekly_total["total_decimal_hours"]
        }
        
        return tasks, totals_row, weekly_total

    def _extract_date(self, text: str) -> str:
        """Extract date from text"""
        # Look for date patterns like "8/15/2025"
        date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}-\d{1,2}-\d{4})',
            r'Date:\s*(\d{1,2}/\d{1,2}/\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return "Unknown"

    def _convert_time_to_decimal(self, time_str: str) -> float:
        """Convert time format (7:30) to decimal hours (7.5)"""
        try:
            if ':' in time_str:
                hours, minutes = map(int, time_str.split(':'))
                return hours + minutes / 60
            else:
                return float(time_str) if time_str else 0.0
        except:
            return 0.0

    def _convert_date_to_iso(self, date_str: str) -> str:
        """Convert date format (11-Aug-25) to ISO format (2025-08-11)"""
        try:
            # Handle format like "11-Aug-25"
            if '-' in date_str:
                parts = date_str.split('-')
                if len(parts) == 3:
                    day, month, year = parts
                    # Convert month name to number
                    month_map = {
                        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                    }
                    month_num = month_map.get(month, '01')
                    # Handle 2-digit year
                    if len(year) == 2:
                        year = '20' + year
                    return f"{year}-{month_num}-{day.zfill(2)}"
        except:
            pass
        return "Unknown"

    # Legacy methods for backward compatibility
    def _extract_employee_name(self, tables) -> str:
        """Extract employee name from tables"""
        if len(tables) >= 2:
            table2 = tables[1]
            for row in table2:
                if row and len(row) >= 2 and 'name' in str(row[0]).lower():
                    name = str(row[1]).strip()
                    if name and name.lower() not in ['', 'none', 'n/a']:
                        return name
        return "Unknown"

    def _extract_week_worked(self, text: str) -> str:
        """Extract week worked from PDF text"""
        pattern = r'(\d{1,2}-[A-Za-z]{3}-\d{2,4})\s*to\s*(\d{1,2}-[A-Za-z]{3}-\d{2,4})'
        match = re.search(pattern, text)
        if match:
            start_date = match.group(1)
            end_date = match.group(2)
            return f"{start_date} to {end_date}"
        
        dates = re.findall(r'\d{1,2}-[A-Za-z]{3}-\d{2,4}', text)
        if len(dates) >= 2:
            return f"{dates[0]} to {dates[-1]}"
        
        return "Unknown"

    def _extract_email_address(self, text: str) -> str:
        """Extract expected email address"""
        pattern = r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return "Unknown"

    def _extract_email_subject(self, text: str) -> str:
        """Extract expected email subject"""
        pattern = r"Subject\s*:\s*([^\n]+)"
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return "Timesheet Submission"

    def _extract_date_received(self, text: str) -> str:
        """Extract date received"""
        pattern = r"(\d{4}-\d{2}-\d{2})"
        match = re.search(pattern, text)
        if match:
            return f"{match.group(1)}, link_to_email_here"
        return "Unknown, link_to_email_here"

    def _extract_contract_particulars(self, tables) -> Dict[str, str]:
        """Extract contract particulars from tables"""
        contract_info = {
            "employee_name": "Unknown",
            "company": "Unknown", 
            "po_number": "Unknown",
            "customer": "Unknown"
        }
        
        if len(tables) >= 1:
            table1 = tables[0]
            for row in table1:
                if row and len(row) >= 2:
                    key = str(row[0]).lower().strip()
                    value = str(row[1]).strip()
                    
                    if 'po number' in key:
                        contract_info["po_number"] = value
                    elif 'client' in key:
                        contract_info["customer"] = value
        
        if len(tables) >= 2:
            table2 = tables[1]
            for row in table2:
                if row and len(row) >= 2:
                    key = str(row[0]).lower().strip()
                    value = str(row[1]).strip()
                    
                    if 'name' in key:
                        contract_info["employee_name"] = value
                    elif 'company' in key:
                        contract_info["company"] = value
        
        return contract_info

    def _extract_table_data(self, tables, text: str) -> list:
        """Extract table data from PDF using pdfplumber's table extraction"""
        table_data = []
        
        try:
            if tables and len(tables) >= 4:
                daily_hours = self._extract_daily_hours_from_work_periods_table(tables[2])
                total_hours = self._extract_total_hours_from_task_summary_table(tables[3])
                
                if daily_hours:
                    week_info = self._extract_week_worked(text)
                    table_data.append({
                        "data_point": "Week Worked",
                        "extracted": week_info,
                        "expected": week_info,
                        "previous": "4-10 August 2025"
                    })
                    
                    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    for day in days:
                        day_short = day[:3].lower()
                        if day_short in daily_hours:
                            hours = daily_hours[day_short]
                            table_data.append({
                                "data_point": f"{day} Hours",
                                "extracted": hours,
                                "expected": "8hrs",
                                "previous": hours
                            })
                        else:
                            table_data.append({
                                "data_point": f"{day} Hours",
                                "extracted": "0hrs",
                                "expected": "0hrs",
                                "previous": "0hrs"
                            })
                    
                    if total_hours:
                        table_data.append({
                            "data_point": "Total Hours",
                            "extracted": total_hours,
                            "expected": "40hrs",
                            "previous": total_hours
                        })
            
            if not table_data:
                table_data = self._extract_from_text(text)
                
        except Exception as e:
            print(f"Error extracting tables: {e}")
            table_data = self._extract_from_text(text)
        
        return table_data

    def _extract_daily_hours_from_work_periods_table(self, table) -> dict:
        """Extract daily hours from the work periods table (table 3)"""
        daily_hours = {}
        
        try:
            total_daily_col_index = 8
            
            for row in table:
                if not row or len(row) <= total_daily_col_index:
                    continue
                
                first_cell = str(row[0]).strip().lower()
                
                day_mapping = {
                    'monday': 'mon',
                    'tuesday': 'tues', 
                    'wednesday': 'wed',
                    'thursday': 'thu',
                    'friday': 'fri',
                    'saturday': 'sat',
                    'sunday': 'sun'
                }
                
                if first_cell in day_mapping:
                    day_short = day_mapping[first_cell]
                    
                    total_cell = row[total_daily_col_index]
                    if total_cell:
                        time_value = str(total_cell).strip()
                        if re.search(r'\d+:\d+', time_value):
                            hours = self._convert_time_to_hours(time_value)
                            daily_hours[day_short] = hours
        
        except Exception as e:
            print(f"Error extracting daily hours from work periods table: {e}")
        
        return daily_hours

    def _extract_total_hours_from_task_summary_table(self, table) -> str:
        """Extract total hours from the task summary table (table 4)"""
        total_hours = None
        
        try:
            for row in table:
                if not row:
                    continue
                
                first_cell = str(row[0]).strip().lower()
                if 'total hours' in first_cell:
                    if len(row) > 7:
                        total_cell = row[7]
                        if total_cell:
                            time_value = str(total_cell).strip()
                            if re.search(r'\d+:\d+', time_value):
                                total_hours = f"{time_value}hrs"
                    break
        
        except Exception as e:
            print(f"Error extracting total hours from task summary table: {e}")
        
        return total_hours

    def _convert_time_to_hours(self, time_str: str) -> str:
        """Convert time format (7:30) to hours format (7.5hrs)"""
        try:
            if ':' in time_str:
                hours, minutes = map(int, time_str.split(':'))
                decimal_hours = hours + minutes / 60
                return f"{decimal_hours:.1f}hrs"
            elif 'hrs' in time_str.lower():
                return time_str
            else:
                return f"{time_str}hrs"
        except:
            return f"{time_str}hrs"

    def _extract_from_text(self, text: str) -> list:
        """Fallback method to extract data from text when tables are not available"""
        table_data = []
        
        try:
            week_pattern = r'(\d{1,2}-\d{1,2}\s+[A-Za-z]+\s+\d{4})'
            week_match = re.search(week_pattern, text)
            if week_match:
                week_info = week_match.group(1)
                table_data.append({
                    "data_point": "Week Worked",
                    "extracted": week_info,
                    "expected": week_info,
                    "previous": "4-10 August 2025"
                })
            
            total_pattern = r'Total\s+Hours?\s*:?\s*(\d+(?:\.\d+)?)\s*hrs?'
            total_match = re.search(total_pattern, text, re.IGNORECASE)
            if total_match:
                total_hours = f"{total_match.group(1)}hrs"
                table_data.append({
                    "data_point": "Total Hours",
                    "extracted": total_hours,
                    "expected": "40hrs",
                    "previous": total_hours
                })
            
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for day in days:
                day_pattern = rf'{day}.*?(\d+(?:\.\d+)?)\s*hrs?'
                day_match = re.search(day_pattern, text, re.IGNORECASE)
                if day_match:
                    hours = f"{day_match.group(1)}hrs"
                    table_data.append({
                        "data_point": f"{day} Hours",
                        "extracted": hours,
                        "expected": "8hrs",
                        "previous": hours
                    })
        
        except Exception as e:
            print(f"Error extracting from text: {e}")
        
        return table_data
