from odoo import models


class WageHistorySummaryXlsx(models.AbstractModel):
    _name = 'report.payroll_wage_history.wage_history_summary_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('Wage history summary')
        title_format = workbook.add_format(
            {
                'font_size': 14,
                'align': 'center',
                'font': 'Times new roman',
                'bold': True,
                'border': True})
        date_format = workbook.add_format(
            {
                'font_size': 12,
                # 'align': 'center',
                'font': 'Times new roman',
            })
        header_format = workbook.add_format(
            {
                'font_size': 13,
                'align': 'left',
                'font': 'Times new roman',
                'bold': True,
                'border': True})
        table_format = workbook.add_format(
            {
                'font_size': 12,
                'align': 'left',
                'font': 'Times new roman',
                'border': True})
        number_format = workbook.add_format(
            {
                'font_size': 12,
                'align': 'right',
                'font': 'Times new roman',
                'border': True})
        index_format = workbook.add_format(
            {
                'font_size': 12,
                'align': 'center',
                'font': 'Times new roman',
                'border': True})
        sheet.set_column(0, 5, 25)
        sheet.set_row(0, 30)
        sheet.set_row(3, 30)

        sheet.write('B2', 'Từ ngày', date_format)
        sheet.write('D2', 'Đến ngày', date_format)

        name_col = (
            'STT \n NO',
            'NHÂN VIÊN \n EMPLOYEE NAME',
            'MỨC LƯƠNG HIỆN TẠI \n CURRENT WAGE',
            'LƯƠNG TRƯỚC ĐÓ \n PREVIOUS WAGE',
            'MỨC TĂNG(%) \n RAISE(%)',
            'ÁP DỤNG TỪ THÁNG \n EFFECTIVE MONTH'
        )
        sheet.write_row('A4', name_col, header_format)

        for rec in partners:
            date_title = f'{rec.to_date.month}/{rec.to_date.year}'
            from_date = f'''
            {rec.from_date.day}/{rec.from_date.month}/{rec.from_date.year}'''
            to_date = f'''
            {rec.to_date.day}/{rec.to_date.month}/{rec.to_date.year}'''

            sheet.merge_range(
                'A1:F1',
                'BÁO CÁO LỊCH SỬ THAY ĐỔI LƯƠNG NHÂN VIÊN NĂM ' + date_title,
                title_format)
            sheet.write('C2', from_date, date_format)
            sheet.write('E2', to_date, date_format)
            for index, wage_history in enumerate(rec.wage_history_ids):
                final_row = len(rec.wage_history_ids)
                name = wage_history.employee_id.name
                current = wage_history.current_payroll_wage
                previous = wage_history.previous_payroll_wage
                percentage = wage_history.percentage
                effective_date = wage_history.effective_date
                date = f'{effective_date.month}/{effective_date.year}'
                sheet.write(4 + index, 0, index + 1, index_format)
                sheet.write(4 + index, 1, name, table_format)
                sheet.write(4 + index, 2, current, number_format)
                sheet.write(4 + index, 3, previous, number_format)
                sheet.write(4 + index, 4, percentage, number_format)
                sheet.write(4 + index, 5, date, number_format)

        footer_left = ('Người lập bảng \n(ghi rõ họ tên)')
        footer_right = ('Giám đốc nhân sự \n(Kí rõ họ tên)')
        sheet.set_row(6 + final_row, 25)
        sheet.write(6 + final_row, 1, footer_left, table_format)
        sheet.write(6 + final_row, 5, footer_right, table_format)
