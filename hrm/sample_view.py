import mimetypes
import os
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from tablib import Dataset
from django.utils.crypto import get_random_string
from .models import *

from hrm.models import Loan_Table


def export(request):
    person_resource = Loan_Table()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response


def simple_upload(request):
    if request.method == 'POST':
        person_resource = Loan_Table()
        dataset = Dataset()

        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read(), format='xlsx')

        DATE = datetime.now().strftime("%Y-%m-%d")
        TIME = datetime.now().strftime("%H:%m")
        success_message = " NO CREATED EMPLOYEE"
        error_message = " SUCCESSFULLY  CREATED ALL EMPLOYEE "
        emp_count = 0
        error_emp_count = 0
        succes_emp_count = 0
        for data in imported_data:
            error = 0
            count = 0
            emp_count = emp_count + 1
            print(emp_count)
            bio_data_submission_date = "none"
            Category = "none"
            Issue_Date = "none"
            Valid_Date = "none"
            salutation = "none"
            age = "none"
            Birth_Place = "none"
            shoe_size = "none"
            waist = "none"
            height = "none"
            weight = "none"
            chest = "none"
            t_shirt_size = "none"
            thouser_size = "none"
            branch_name = "none"
            pay_mode = "none"
            passbook_name = "none"
            JOIN_ACCOUNT_NO = "none"
            JOIN_ACCOUNT_BANK_NAME = "none"
            JOIN_ACCOUNT_NAME = "none"
            JOIN_ACCOUNT_BRANCH_NAME = "none"
            STREET = "none"
            DISTRICT = "none"
            PIN_CODE = "none"
            TELEPHONE = "none"
            DURATION = "none"
            STATE = "none"
            per_street = "none"
            per_district = "none"
            per_pin_code = "none"
            per_duration = "none"
            per_state = "none"
            experiance = "none"
            SPECIAL_ALLOWANCES = 0
            CONVEYANCE_TA = 0
            OTHER_ALLOWANCES = 0
            OT_PER_HRS_PAY = 0
            SITE_ALLOWANCES = 0
            EXTRA_SHIFT_PER_HRS_PAY = 0
            INCENTIVE = 0
            LEAVE_TRAVEL_ALLOWANCES = 0
            MEDICAL_ALLOWANCES = 0
            CHILD_EDUCATIONS_ALLOWANCES = 0
            ATTENDANCE_BONUS = 0
            ATTENDANCE_INCENTIVE = 0
            OTHER_INCENTIVE = 0
            MONTHLY_LEAVE_WAGES = 0
            RELIVER_DUTY_WAGES = 0
            ARREARS_WAGES = 0
            INCOME_TAX = 0
            LOAN = 0
            SALARY_ADVANCE = 0
            OTHER_DEDUCTIONS = 0
            UNIFORM_DEDUCTIONS = 0
            VERIFICATION_NO = "none"
            VERIFICATION_DATE = "none"
            CRIMINOLOGY = "none"
            PV_SEND_DATE = "none"
            PV_RETURN_DATE = "none"
            NAME_OF_THE_POLICE = "none"
            IDENTITY_SIGN = "none"
            PV_VALID_DATE = "none"
            REMARK = "none"
            NOMINE_NAME = "none"
            NOMINE_RELATION = "none"
            for data1 in data:
                if data1 is None:
                    if 0 <= count < 8 or count == 9 or 14 <= count < 19 or 20 <= count < 24 or \
                            count == 25 or count == 26 or 34 <= count < 43 or count == 50 \
                            or count == 55 or count == 56 or count == 59 or count == 66 or \
                            count == 67 or count == 68:
                        error = error + 1
                count = count + 1
            count = 0
            if error == 0:
                print(data)
                country = data[0]
                state = data[1]
                district = data[2]
                branch = data[3]
                area = data[4]
                client = data[5]
                unit = data[6]
                date_of_join = data[7]
                if data[8] is not None:
                    bio_data_submission_date = data[8]
                Designation = data[9]
                if data[10] is not None:
                    Category = data[10]
                if data[11] is not None:
                    Issue_Date = data[11]
                if data[12] is not None:
                    Valid_Date = data[12]
                if data[13] is not None:
                    salutation = data[13]
                employee_name = data[14]
                dob = data[15]
                marital_status = data[16]
                gender = data[17]
                contact_no = data[18]
                if data[19] is not None:
                    age = data[19]
                Wife_Husband_Name = data[20]
                Father_Name = data[21]
                Mother_Name = data[22]
                Highest_Education = data[23]
                if data[24] is not None:
                    Birth_Place = data[24]
                Nationality = data[25]
                Blood_Group = data[26]
                if data[27] is not None:
                    shoe_size = data[27]
                if data[28] is not None:
                    waist = data[28]
                if data[29] is not None:
                    height = data[29]
                if data[30] is not None:
                    weight = data[30]
                if data[31] is not None:
                    chest = data[31]
                if data[32] is not None:
                    t_shirt_size = data[32]
                if data[33] is not None:
                    thouser_size = data[33]
                Pan_No = data[34]
                PF_No = data[35]
                ESI_No = data[36]
                AADHAR_No = data[37]
                UAN_No = data[38]
                ID_Card_No = data[39]
                ACCOUNT_NO = data[40]
                BANK_NAME = data[41]
                IFSC_CODE = data[42]
                if data[43] is not None:
                    branch_name = data[43]
                if data[44] is not None:
                    pay_mode = data[44]
                if data[45] is not None:
                    passbook_name = data[45]
                if data[46] is not None:
                    JOIN_ACCOUNT_NO = data[46]
                if data[47] is not None:
                    JOIN_ACCOUNT_BANK_NAME = data[47]
                if data[48] is not None:
                    JOIN_ACCOUNT_NAME = data[48]
                if data[49] is not None:
                    JOIN_ACCOUNT_BRANCH_NAME = data[49]
                ADDRESS = data[50]
                if data[51] is not None:
                    STREET = data[51]
                if data[52] is not None:
                    DISTRICT = data[52]
                if data[53] is not None:
                    PIN_CODE = data[53]
                if data[54] is not None:
                    TELEPHONE = data[54]
                MOBILE_NO = data[55]
                EMAIL_ID = data[56]
                if data[57] is not None:
                    DURATION = data[57]
                if data[58] is not None:
                    STATE = data[58]
                PERMANENT_ADDRESS = data[59]
                if data[60] is not None:
                    per_street = data[60]
                if data[61] is not None:
                    per_district = data[61]
                if data[62] is not None:
                    per_pin_code = data[62]
                if data[63] is not None:
                    per_duration = data[63]
                if data[64] is not None:
                    per_state = data[64]
                if data[65] is not None:
                    experiance = data[65]
                basic = data[66]
                DA = data[67]
                HOUSE = data[68]
                fixed_salary = basic + DA + HOUSE
                if data[69] is not None:
                    SPECIAL_ALLOWANCES = data[69]
                if data[70] is not None:
                    CONVEYANCE_TA = data[70]
                if data[71] is not None:
                    OTHER_ALLOWANCES = data[71]
                if data[72] is not None:
                    OT_PER_HRS_PAY = data[72]
                if data[73] is not None:
                    SITE_ALLOWANCES = data[73]
                if data[74] is not None:
                    EXTRA_SHIFT_PER_HRS_PAY = data[74]
                if data[75] is not None:
                    INCENTIVE = data[75]
                if data[76] is not None:
                    LEAVE_TRAVEL_ALLOWANCES = data[76]
                if data[77] is not None:
                    MEDICAL_ALLOWANCES = data[77]
                if data[78] is not None:
                    CHILD_EDUCATIONS_ALLOWANCES = data[78]
                if data[79] is not None:
                    ATTENDANCE_BONUS = data[79]
                if data[80] is not None:
                    ATTENDANCE_INCENTIVE = data[80]
                if data[81] is not None:
                    OTHER_INCENTIVE = data[81]
                if data[82] is not None:
                    MONTHLY_LEAVE_WAGES = data[82]
                if data[83] is not None:
                    RELIVER_DUTY_WAGES = data[83]
                if data[84] is not None:
                    ARREARS_WAGES = data[84]
                if data[87] is not None:
                    INCOME_TAX = data[87]
                if data[88] is not None:
                    LOAN = data[88]
                if data[89] is not None:
                    SALARY_ADVANCE = data[89]
                if data[90] is not None:
                    OTHER_DEDUCTIONS = data[90]
                if data[91] is not None:
                    UNIFORM_DEDUCTIONS = data[91]
                if data[92] is not None:
                    VERIFICATION_NO = data[92]
                if data[93] is not None:
                    VERIFICATION_DATE = data[93]
                if data[94] is not None:
                    CRIMINOLOGY = data[94]
                if data[95] is not None:
                    PV_SEND_DATE = data[95]
                if data[96] is not None:
                    PV_RETURN_DATE = data[96]
                if data[97] is not None:
                    NAME_OF_THE_POLICE = data[97]
                if data[98] is not None:
                    IDENTITY_SIGN = data[98]
                if data[99] is not None:
                    PV_VALID_DATE = data[99]
                if data[100] is not None:
                    REMARK = data[100]
                if data[101] is not None:
                    NOMINE_NAME = data[101]
                if data[102] is not None:
                    NOMINE_RELATION = data[102]
                try:
                    aadthar = EMP_PERSONAL_DETAILS.objects.get(PAN_NO=Pan_No)
                    error_emp_count = error_emp_count + 1
                    if data[14] is not None:
                        if error_emp_count == 1:
                            print(aadthar.AADHAR_NO)
                            error_message = " EMPLOYEE " + data[14] + "  IS ALREADY EXIST "
                        else:
                            error_message = error_message + ", " + " EMPLOYEE " + data[14] + " IS ALREADY EXIST "
                    else:
                        if error_emp_count == 1:
                            print(aadthar.AADHAR_NO)
                            error_message = " EMPLOYEE " + str(emp_count) + "  IS ALREADY EXIST "
                        else:
                            error_message = error_message + ", " + " EMPLOYEE " + str(emp_count) + " IS ALREADY EXIST "
                except EMP_PERSONAL_DETAILS.DoesNotExist:
                    try:
                        last_id = new_emp_reg.objects.latest('ID')
                        print(type(last_id.EMP_CODE), "LAST ID try")
                        increse = int(last_id.EMP_CODE) + 1
                        print(increse)
                        if increse < 10:
                            new_id = "000" + str(increse)
                        elif increse >= 10 and increse < 100:
                            new_id = "00" + str(increse)
                        elif increse >= 100 and increse < 1000:
                            new_id = "0" + str(increse)
                        elif increse >= 1000:
                            new_id = str(increse)
                    except new_emp_reg.DoesNotExist:
                        new_id = "0001"
                    succes_emp_count = succes_emp_count + 1
                    if data[14] is not None:
                        if succes_emp_count == 1:
                            success_message = "Employee   " + data[14] + "'S Code is " + new_id
                        else:
                            success_message = success_message + ", " + "Employee   " + data[14] + "'S Code is " + new_id
                    else:
                        if succes_emp_count == 1:
                            success_message = "Employee   " + str(emp_count) + "'S Code is " + new_id
                        else:
                            success_message = success_message + ", " + "Employee   " + str(
                                emp_count) + "'S Code is " + new_id
                    print(bio_data_submission_date)
                    new_emp_register = new_emp_reg(
                        EMP_NAME=employee_name,
                        EMP_CODE=new_id,
                        DOB=dob,
                        GENDER=gender,
                        REG_DATE=DATE,
                        REG_TIME=TIME,
                        SALUTATION=salutation,
                        MARITAL_STATUS=marital_status,
                        MOBILE_NO=contact_no,
                        AGE=age,
                        EXPERIANCE=experiance,
                    )
                    new_emp_register.save()
                    emp_company_reg = EMP_COMPANY_DETAILS(
                        EMP_CODE=new_id,
                        EMP_LINK=new_emp_register,
                        COUNTRY=country,
                        STATE=state,
                        DISTRICT=district,
                        BRANCH=branch,
                        AREA=area,
                        CLIENT=client,
                        UNIT=unit,
                        DATE_OF_JOIN=date_of_join,
                        BIO_DATE_SUB_DATE=bio_data_submission_date,
                        DESIGNATION=Designation,
                        CATEGORY=Category,
                        ISSUE_DATE=Issue_Date,
                        VAILD_DATE=Valid_Date
                    )
                    emp_company_reg.save()

                    emp_per_details = EMP_PERSONAL_DETAILS(
                        EMP_CODE=new_id,
                        EMP_LINK=emp_company_reg,
                        WIFE_HUSBAND_NAME=Wife_Husband_Name,
                        FATHER_NAME=Father_Name,
                        MOTHER_NAME=Mother_Name,
                        HIGHEST_EDUCATION=Highest_Education,
                        BIRTH_PLACE=Birth_Place,
                        PAN_NO=Pan_No,
                        PF_NO=PF_No,
                        ESI_NO=ESI_No,
                        AADHAR_NO=AADHAR_No,
                        UAN_NO=UAN_No,
                        ID_CARD_NO=ID_Card_No,
                        NATIONALITY=Nationality,
                        BLOOD_GROUP=Blood_Group,
                        SHOE_SIZE=shoe_size,
                        WAIST=waist,
                        HEIGHT=height,
                        WEIGHT=weight,
                        CHEST=chest,
                        T_SHIRT_SIZE=t_shirt_size,
                        THOUSER_SIZE=thouser_size
                    )
                    emp_per_details.save()

                    emp_comm_details = EMP_COMMUNICATION_DETAILS(
                        EMP_CODE=new_id,
                        EMP_LINK=emp_per_details,
                        ADDRESS=ADDRESS,
                        STREET=STREET,
                        DISTRICT=DISTRICT,
                        PINCODE=PIN_CODE,
                        TELEPHONE=TELEPHONE,
                        MOBILE_NO=MOBILE_NO,
                        EMAIL_ID=EMAIL_ID,
                        DURATION=DURATION,
                        STATE=STATE,
                        PER_ADDRESS=PERMANENT_ADDRESS,
                        PER_STREET=per_street,
                        PER_DISTRICT=per_district,
                        PER_PINCODE=per_pin_code,
                        PER_DURATION=per_duration,
                        PER_STATE=per_state
                    )
                    emp_comm_details.save()

                    emp_bank_details = EMP_BANK_DETAILS(
                        EMP_CODE=new_id,
                        EMP_LINK=emp_comm_details,
                        ACCOUNT_NO=ACCOUNT_NO,
                        BANK_NAME=BANK_NAME,
                        IFSC_CODE=IFSC_CODE,
                        BRANCH=branch_name,
                        PAYMENT_MODE=pay_mode,
                        PASSBOOK_NAME=passbook_name,
                        JOIN_ACC_NO=JOIN_ACCOUNT_NO,
                        JOIN_ACC_NAME=JOIN_ACCOUNT_NAME,
                        JOIN_ACC_BRANCH_NAME=JOIN_ACCOUNT_BRANCH_NAME,
                        JOIN_ACC_BANK_NAME=JOIN_ACCOUNT_BANK_NAME
                    )
                    emp_bank_details.save()

                    emp_salary_details = salary_details(
                        EMP_CODE=new_id,
                        EMP_LINK=emp_bank_details,
                        FIXED_SALARY=fixed_salary,
                        MONTH_SALARY=fixed_salary,
                        BASIC=basic,
                        DEARANCE_ALLOWANCES=DA,
                        SPECIAL_ALLOWANCES=SPECIAL_ALLOWANCES,
                        HOUSE_RENT_ALLOWANCES=HOUSE,
                        CONVEYANCE=CONVEYANCE_TA,
                        OTHER_ALLOWANCES=OTHER_ALLOWANCES,
                        OVERTIME_AMOUNT=0,
                        SITE_ALLOWANCES=SITE_ALLOWANCES,
                        SHIFT_ALLOWANCES_AMOUNT=EXTRA_SHIFT_PER_HRS_PAY,
                        INCENTIVE=INCENTIVE,
                        LEAVE_TRAVEL_ALLOWANCES=LEAVE_TRAVEL_ALLOWANCES,
                        MEDICAL_ALLOWANCES=MEDICAL_ALLOWANCES,
                        CHILD_EDUCATIONS_ALLOWANCES=CHILD_EDUCATIONS_ALLOWANCES,
                        ATTENDANCE_BONUS=ATTENDANCE_BONUS,
                        ATTENDANCE_INCENTIVE=ATTENDANCE_INCENTIVE,
                        MONTHLY_BOUNS=0,
                        EXTRA_BOUNS=OTHER_INCENTIVE,
                        MONTHLY_LEAVE_WAGES=MONTHLY_LEAVE_WAGES,
                        ESIC=0,
                        RELIVER_DUTY_WAGES=RELIVER_DUTY_WAGES,
                        ARREARS_WAGES=ARREARS_WAGES,
                        PROFESSIONAL_TAX=0,
                        LABOUR_WELFARE_FUND=0,
                        INCOME_TAX=INCOME_TAX,
                        LOAN=LOAN,
                        SALARY_ADVANCE=SALARY_ADVANCE,
                        OTHER_DEDUCTION=OTHER_DEDUCTIONS,
                        UNIFORM_DEDUCTION=UNIFORM_DEDUCTIONS,
                        TOTAL_EARN=0,
                        TOTAL_DEDUCATION=0,
                        NET_PAY=0,
                        PROVIDENT_FUND=0,
                        SALARY_UPDATE_DATE="NO UPDATED",
                        NAMINE_E_NAME=NOMINE_NAME,
                        NAMINE_E_RELATIONS=NOMINE_RELATION,
                    )
                    emp_salary_details.save()
                    emp_daily_attendance = EMP_DAILY_ATTENDANCE_UPDATED(
                        EMP_CODE=new_id,
                        EMP_NAME=employee_name,
                        DESIGNATION=Designation,
                        IN_TIME="00.00",
                        OUT_TIME="00.00",
                        ATTENDANCE_STATUS="NONE",
                        LAST_UPDATE_DATE="NO UPDATED",
                    )
                    emp_daily_attendance.save()
                    emp_police_details = EMP_POLICE_VERFICATION(
                        EMP_CODE=new_id,
                        EMP_BANK=emp_bank_details,
                        EMP_COMM=emp_comm_details,
                        EMP_PER=emp_per_details,
                        EMP_COMPANY=emp_company_reg,
                        EMP_SAL=emp_salary_details,
                        NEW_EMP=new_emp_register
                    )
                    emp_police_details.save()

                    EMP_POLICE_VERFICATION.objects.filter(EMP_CODE=new_id).update(
                        VERFICATION_NO=VERIFICATION_NO,
                        VERFICATION_DATE=VERIFICATION_DATE,
                        CRIMINOLOGY=CRIMINOLOGY,
                        PV_SEND_DATE=PV_SEND_DATE,
                        PV_RETURN_DATE=PV_RETURN_DATE,
                        NAME_OF_POLICE_THANA=NAME_OF_THE_POLICE,
                        IDENTITY_SIGN=IDENTITY_SIGN,
                        PV_VALID_UPTO=PV_VALID_DATE,
                        REMARK_BY_THANA=REMARK,
                    )
            else:
                error_emp_count = error_emp_count + 1
                if data[14] is not None:
                    if error_emp_count == 1:
                        error_message = " EMPLOYEE " + data[14] + " PLZ ENTER  YOUR DATA PROPERLY"
                    else:
                        error_message = error_message + ", " + " EMPLOYEE " + data[
                            14] + " PLZ ENTER  YOUR DATA PROPERLY"
                else:
                    if error_emp_count == 1:
                        print(emp_count, "1")
                        error_message = " EMPLOYEE " + str(emp_count) + " PLZ ENTER  YOUR DATA PROPERLY"
                    else:
                        print(emp_count, "2")
                        error_message = error_message + ", " + " EMPLOYEE " + str(
                            emp_count) + " PLZ ENTER  YOUR DATA PROPERLY"

        return render(request, 'excel_file.html', {'not_insert': error_message, 'insert': success_message})
    else:
        return render(request, 'excel_file.html')


def monthly_Att_upload(request):
    if request.method == 'POST':
        person_resource = Loan_Table()
        dataset = Dataset()

        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read(), format='xlsx')
        print(imported_data, "importted")
        success_message = " NO UPDATE ATTENTDANCE FOR EMPLOYEE"
        error_message = " SUCCESSFULLY  UPDATED ATTENTDANCE ALL EMPLOYEE "
        emp_count = 0
        error_emp_count = 0
        succes_emp_count = 0
        for data in imported_data:
            print(data)
            error = 0
            count = 0
            emp_count = emp_count + 1
            print(emp_count)
            EXTRA_SHIFT_TIME = 0
            emp_name = str(emp_count)
            over_time = 0
            for value in data:
                count = count + 1
                if value is None:
                    if count != 5 and count != 2 and count != 4:
                        error = error + 1
                        print("aa", count)
            if error == 0:
                if data[4] is not None:
                    EXTRA_SHIFT_TIME = data[4]
                if data[1] is not None:
                    emp_name = data[1]
                if data[3] is not None:
                    over_time = data[3]
                emp_code = data[0]
                print(type(emp_code))
                try:
                    emp_code = int(emp_code)
                    if emp_code < 10:
                        emp_code = "000" + str(emp_code)
                    elif emp_code >= 10 and emp_code < 100:
                        emp_code = "00" + str(emp_code)
                    elif emp_code >= 100 and emp_code < 1000:
                        emp_code = "0" + str(emp_code)
                    elif emp_code >= 1000:
                        emp_code = emp_code
                    day_present = data[2]
                    year = data[5]
                    month = data[6]
                    print(emp_code)
                    try:
                        emp_code_check = new_emp_reg.objects.get(EMP_CODE=emp_code)
                        try:
                            print("atten try")
                            emp_code_check = Monthly_Attendance_Table.objects.get(EMP_CODE=emp_code, MONTH=month,
                                                                                  YEAR=year)
                            Monthly_Attendance_Table.objects.filter(EMP_CODE=emp_code, MONTH=month,
                                                                    YEAR=year).update(
                                DAYS_PRESENT=day_present,
                                OVERTIME_HRS=over_time,
                                SHIFT_ALLOWANCES_HRS=EXTRA_SHIFT_TIME,
                            )
                            succes_emp_count = succes_emp_count + 1
                            print(succes_emp_count)
                            if succes_emp_count == 1:
                                print(succes_emp_count, "111")
                                success_message = "Employee " + emp_name + " Your Attentdance Data is Successfully Updated"
                            else:
                                print(succes_emp_count, "222")
                                success_message = success_message + "," + "Employee " + emp_name + " Your Attentdance Data is Successfully Updated"

                        except Monthly_Attendance_Table.DoesNotExist:
                            print("atten else")
                            succes_emp_count = succes_emp_count + 1
                            if succes_emp_count == 1:
                                success_message = "Employee " + emp_name + " Your  Attentdance Data is Successfully Insert"
                            else:
                                success_message = success_message + ", " + "Employee " + emp_name + " Your Attentdance Data is Successfully Insert"
                            # data1 = salary_details.objects.filter(EMP_CODE=emp_code)
                            print(emp_code_check, "---------")

                            emp_monthly_attentdence = Monthly_Attendance_Table(
                                EMP_CODE=emp_code,
                                DAYS_PRESENT=day_present,
                                OVERTIME_HRS=over_time,
                                SHIFT_ALLOWANCES_HRS=EXTRA_SHIFT_TIME,
                                MONTH=month,
                                YEAR=year
                            )
                            emp_monthly_attentdence.save()
                        month_year = month + "-" + str(year)
                        print(month_year)
                        emp_salary_details = salary_details.objects.get(EMP_CODE=emp_code)
                        FIXED_SALARY = emp_salary_details.FIXED_SALARY
                        basic = int(emp_salary_details.BASIC)
                        da = int(emp_salary_details.DEARANCE_ALLOWANCES)
                        oneday_salary = int(FIXED_SALARY) / 30
                        onehr_salary = (int(FIXED_SALARY) / 30) / 8
                        over_time_sal = over_time * 2
                        emp_over_time_amount = onehr_salary * over_time_sal
                        month_salary = oneday_salary * day_present

                        LEAVE_TRAVEL = basic / 12
                        PROFESSIONAL_TAX = (basic * 0.25) / 100
                        LABOUR_WELFARE_FUND = (basic * 0.10) / 100
                        PENSION_AMOUNT = (basic * 8.33) / 100
                        monthly_bonus = (basic * 8.33) / 100
                        PROVIDENTFUND = (basic * 3.67) / 100
                        total_earn = month_salary + emp_over_time_amount + LEAVE_TRAVEL + monthly_bonus \
                                     + int(emp_salary_details.SPECIAL_ALLOWANCES) + int(
                            emp_salary_details.CONVEYANCE) + int(emp_salary_details.OTHER_ALLOWANCES) \
                                     + int(emp_salary_details.SITE_ALLOWANCES) + int(
                            emp_salary_details.SHIFT_ALLOWANCES_AMOUNT) + int(
                            emp_salary_details.INCENTIVE) \
                                     + int(emp_salary_details.MEDICAL_ALLOWANCES) + int(
                            emp_salary_details.CHILD_EDUCATIONS_ALLOWANCES) + int(
                            emp_salary_details.ATTENDANCE_BONUS) \
                                     + int(emp_salary_details.ATTENDANCE_INCENTIVE) + int(
                            emp_salary_details.EXTRA_BOUNS) + int(
                            emp_salary_details.RELIVER_DUTY_WAGES) + \
                                     + int(emp_salary_details.ARREARS_WAGES) + int(
                            emp_salary_details.MONTHLY_LEAVE_WAGES)
                        esic = (total_earn * 0.75) / 100
                        total_deducation = PROVIDENTFUND + esic + PENSION_AMOUNT + LABOUR_WELFARE_FUND + PROFESSIONAL_TAX \
                                           + int(emp_salary_details.INCOME_TAX) + int(emp_salary_details.LOAN) + int(
                            emp_salary_details.SALARY_ADVANCE) \
                                           + int(emp_salary_details.OTHER_DEDUCTION) + int(
                            emp_salary_details.UNIFORM_DEDUCTION)
                        net_pay = total_earn - total_deducation

                        try:
                            EMP_SALARY_MAINTAINS.objects.get(EMP_CODE=emp_code, SALARY_UPDATE_DATE=month_year)
                            print("maintains try")
                            EMP_SALARY_MAINTAINS.objects.filter(EMP_CODE=emp_code,
                                                                SALARY_UPDATE_DATE=month_year).update(
                                FIXED_SALARY=FIXED_SALARY,
                                MONTH_SALARY=month_salary,
                                BASIC=basic,
                                DEARANCE_ALLOWANCES=emp_salary_details.DEARANCE_ALLOWANCES,
                                SPECIAL_ALLOWANCES=emp_salary_details.SPECIAL_ALLOWANCES,
                                HOUSE_RENT_ALLOWANCES=emp_salary_details.HOUSE_RENT_ALLOWANCES,
                                CONVEYANCE=emp_salary_details.CONVEYANCE,
                                OTHER_ALLOWANCES=emp_salary_details.OTHER_ALLOWANCES,
                                OVERTIME_AMOUNT="{:.2f}".format(emp_over_time_amount),
                                SITE_ALLOWANCES=emp_salary_details.SITE_ALLOWANCES,
                                SHIFT_ALLOWANCES_AMOUNT=emp_salary_details.SHIFT_ALLOWANCES_AMOUNT,
                                INCENTIVE=emp_salary_details.INCENTIVE,
                                LEAVE_TRAVEL_ALLOWANCES="{:.2f}".format(LEAVE_TRAVEL),
                                MEDICAL_ALLOWANCES=emp_salary_details.MEDICAL_ALLOWANCES,
                                CHILD_EDUCATIONS_ALLOWANCES=emp_salary_details.CHILD_EDUCATIONS_ALLOWANCES,
                                ATTENDANCE_BONUS=emp_salary_details.ATTENDANCE_BONUS,
                                ATTENDANCE_INCENTIVE=emp_salary_details.ATTENDANCE_INCENTIVE,
                                MONTHLY_BOUNS=monthly_bonus,
                                MONTHLY_LEAVE_WAGES=emp_salary_details.MONTHLY_LEAVE_WAGES,
                                PROVIDENT_FUND=PROVIDENTFUND,
                                ESIC="{:.2f}".format(esic),
                                PENSION_AMOUNT="{:.2f}".format(PENSION_AMOUNT),
                                RELIVER_DUTY_WAGES=emp_salary_details.RELIVER_DUTY_WAGES,
                                ARREARS_WAGES=emp_salary_details.ARREARS_WAGES,
                                PROFESSIONAL_TAX="{:.2f}".format(PROFESSIONAL_TAX),
                                LABOUR_WELFARE_FUND="{:.2f}".format(LABOUR_WELFARE_FUND),
                                INCOME_TAX=emp_salary_details.INCOME_TAX,
                                LOAN=emp_salary_details.LOAN,
                                SALARY_ADVANCE=emp_salary_details.SALARY_ADVANCE,
                                OTHER_DEDUCTION=emp_salary_details.OTHER_DEDUCTION,
                                UNIFORM_DEDUCTION=emp_salary_details.UNIFORM_DEDUCTION,
                                TOTAL_EARN="{:.2f}".format(total_earn),
                                TOTAL_DEDUCATION="{:.2f}".format(total_deducation),
                                NET_PAY="{:.2f}".format(net_pay),
                                SALARY_UPDATE_DATE=month_year,
                                EXTRA_BOUNS=emp_salary_details.EXTRA_BOUNS,
                                DAYS_PRESENT=day_present,
                                OVERTIME_HRS=over_time,
                                SHIFT_ALLOWANCES_HRS=EXTRA_SHIFT_TIME,
                            )
                        except EMP_SALARY_MAINTAINS.DoesNotExist:
                            print("maintains else")
                            salary_maintains = EMP_SALARY_MAINTAINS(
                                EMP_CODE=emp_code,
                                FIXED_SALARY=FIXED_SALARY,
                                MONTH_SALARY=month_salary,
                                BASIC=basic,
                                DEARANCE_ALLOWANCES=emp_salary_details.DEARANCE_ALLOWANCES,
                                SPECIAL_ALLOWANCES=emp_salary_details.SPECIAL_ALLOWANCES,
                                HOUSE_RENT_ALLOWANCES=emp_salary_details.HOUSE_RENT_ALLOWANCES,
                                CONVEYANCE=emp_salary_details.CONVEYANCE,
                                OTHER_ALLOWANCES=emp_salary_details.OTHER_ALLOWANCES,
                                OVERTIME_AMOUNT="{:.2f}".format(emp_over_time_amount),
                                SITE_ALLOWANCES=emp_salary_details.SITE_ALLOWANCES,
                                SHIFT_ALLOWANCES_AMOUNT=emp_salary_details.SHIFT_ALLOWANCES_AMOUNT,
                                INCENTIVE=emp_salary_details.INCENTIVE,
                                LEAVE_TRAVEL_ALLOWANCES="{:.2f}".format(LEAVE_TRAVEL),
                                MEDICAL_ALLOWANCES=emp_salary_details.MEDICAL_ALLOWANCES,
                                CHILD_EDUCATIONS_ALLOWANCES=emp_salary_details.CHILD_EDUCATIONS_ALLOWANCES,
                                ATTENDANCE_BONUS=emp_salary_details.ATTENDANCE_BONUS,
                                ATTENDANCE_INCENTIVE=emp_salary_details.ATTENDANCE_INCENTIVE,
                                MONTHLY_BOUNS=monthly_bonus,
                                MONTHLY_LEAVE_WAGES=emp_salary_details.MONTHLY_LEAVE_WAGES,
                                PROVIDENT_FUND=PROVIDENTFUND,
                                ESIC="{:.2f}".format(esic),
                                PENSION_AMOUNT="{:.2f}".format(PENSION_AMOUNT),
                                RELIVER_DUTY_WAGES=emp_salary_details.RELIVER_DUTY_WAGES,
                                ARREARS_WAGES=emp_salary_details.ARREARS_WAGES,
                                PROFESSIONAL_TAX="{:.2f}".format(PROFESSIONAL_TAX),
                                LABOUR_WELFARE_FUND="{:.2f}".format(LABOUR_WELFARE_FUND),
                                INCOME_TAX=emp_salary_details.INCOME_TAX,
                                LOAN=emp_salary_details.LOAN,
                                SALARY_ADVANCE=emp_salary_details.SALARY_ADVANCE,
                                OTHER_DEDUCTION=emp_salary_details.OTHER_DEDUCTION,
                                UNIFORM_DEDUCTION=emp_salary_details.UNIFORM_DEDUCTION,
                                TOTAL_EARN="{:.2f}".format(total_earn),
                                TOTAL_DEDUCATION="{:.2f}".format(total_deducation),
                                NET_PAY="{:.2f}".format(net_pay),
                                SALARY_UPDATE_DATE=month_year,
                                EXTRA_BOUNS=emp_salary_details.EXTRA_BOUNS,
                                DAYS_PRESENT=day_present,
                                OVERTIME_HRS=over_time,
                                SHIFT_ALLOWANCES_HRS=EXTRA_SHIFT_TIME,
                            )
                            salary_maintains.save()

                        salary_details.objects.filter(EMP_CODE=emp_code).update(
                            FIXED_SALARY=FIXED_SALARY,
                            MONTH_SALARY=month_salary,
                            BASIC=basic,
                            DEARANCE_ALLOWANCES=emp_salary_details.DEARANCE_ALLOWANCES,
                            SPECIAL_ALLOWANCES=emp_salary_details.SPECIAL_ALLOWANCES,
                            HOUSE_RENT_ALLOWANCES=emp_salary_details.HOUSE_RENT_ALLOWANCES,
                            CONVEYANCE=emp_salary_details.CONVEYANCE,
                            OTHER_ALLOWANCES=emp_salary_details.OTHER_ALLOWANCES,
                            OVERTIME_AMOUNT="{:.2f}".format(emp_over_time_amount),
                            SITE_ALLOWANCES=emp_salary_details.SITE_ALLOWANCES,
                            SHIFT_ALLOWANCES_AMOUNT=emp_salary_details.SHIFT_ALLOWANCES_AMOUNT,
                            INCENTIVE=emp_salary_details.INCENTIVE,
                            LEAVE_TRAVEL_ALLOWANCES="{:.2f}".format(LEAVE_TRAVEL),
                            MEDICAL_ALLOWANCES=emp_salary_details.MEDICAL_ALLOWANCES,
                            CHILD_EDUCATIONS_ALLOWANCES=emp_salary_details.CHILD_EDUCATIONS_ALLOWANCES,
                            ATTENDANCE_BONUS=emp_salary_details.ATTENDANCE_BONUS,
                            ATTENDANCE_INCENTIVE=emp_salary_details.ATTENDANCE_INCENTIVE,
                            MONTHLY_BOUNS=monthly_bonus,
                            MONTHLY_LEAVE_WAGES=emp_salary_details.MONTHLY_LEAVE_WAGES,
                            PROVIDENT_FUND=PROVIDENTFUND,
                            ESIC="{:.2f}".format(esic),
                            PENSION_AMOUNT="{:.2f}".format(PENSION_AMOUNT),
                            RELIVER_DUTY_WAGES=emp_salary_details.RELIVER_DUTY_WAGES,
                            ARREARS_WAGES=emp_salary_details.ARREARS_WAGES,
                            PROFESSIONAL_TAX="{:.2f}".format(PROFESSIONAL_TAX),
                            LABOUR_WELFARE_FUND="{:.2f}".format(LABOUR_WELFARE_FUND),
                            INCOME_TAX=emp_salary_details.INCOME_TAX,
                            LOAN=emp_salary_details.LOAN,
                            SALARY_ADVANCE=emp_salary_details.SALARY_ADVANCE,
                            OTHER_DEDUCTION=emp_salary_details.OTHER_DEDUCTION,
                            UNIFORM_DEDUCTION=emp_salary_details.UNIFORM_DEDUCTION,
                            TOTAL_EARN="{:.2f}".format(total_earn),
                            TOTAL_DEDUCATION="{:.2f}".format(total_deducation),
                            NET_PAY="{:.2f}".format(net_pay),
                            SALARY_UPDATE_DATE=month_year,
                            EXTRA_BOUNS=emp_salary_details.EXTRA_BOUNS,
                        )
                    except new_emp_reg.DoesNotExist:
                        print("no register")
                        error_emp_count = error_emp_count + 1
                        if error_emp_count == 1:
                            error_message = emp_name + " YOUR CODE IS WRONG  "
                        else:
                            error_message = error_message + "," + emp_name + " YOUR CODE IS WRONG  "
                except ValueError:
                    print("no jdjj")
                    error_emp_count = error_emp_count + 1
                    if error_emp_count == 1:
                        error_message = emp_name + " YOUR CODE IS WRONG  "
                    else:
                        error_message = error_message + "," + emp_name + " YOUR CODE IS WRONG  "
            else:
                error_emp_count = error_emp_count + 1
                if error_emp_count == 1:
                    print(emp_count, "1")
                    error_message = " EMPLOYEE " + emp_name + " PLZ ENTER  YOUR DATA PROPERLY"
                else:
                    print(emp_count, "2")
                    error_message = error_message + ", " + " EMPLOYEE " + emp_name + " PLZ ENTER  YOUR DATA PROPERLY"

        return render(request, 'excel_attendance_file.html', {'not_insert': error_message, 'insert': success_message})
    else:
        return render(request, 'excel_attendance_file.html')


def download_file(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'EMPREG.xlsx'
    # Define the full file path
    filepath = BASE_DIR + '/templates/' + filename

    # Open the file for reading content
    path = open(filepath, "rb")

    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value

    return response


def download_att_file(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'EMPATT.xlsx'
    # Define the full file path
    filepath = BASE_DIR + '/templates/' + filename

    # Open the file for reading content
    path = open(filepath, "rb")

    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response
