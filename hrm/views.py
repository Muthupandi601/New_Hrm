import os
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
from django.utils.crypto import get_random_string
from .models import *
from .forms import CreateUserForm
import smtplib

import mimetypes

from django.shortcuts import render, redirect, get_object_or_404
import json as simplejson
from .models import City, State


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request, '404.html', data)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        reg = "yes"
        form = CreateUserForm()
        if request.method == 'POST':
            print(request.POST.get('sign_up'))
            if request.POST.get('sign_up') == "admin":
                form = CreateUserForm(request.POST)
                if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)

                    return redirect('login')
                else:
                    context = {'form': form, 'reg': reg}
                    return render(request, 'accounts/Sign_up.html', context)
            elif request.POST.get('sign_up') == "user":
                form = CreateUserForm(request.POST)
                print(request.POST.get('is_staff'))
                if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)

                    return redirect('login')
                else:
                    user_reg = "yes"
                    context = {'form': form, 'reg': reg, 'user_reg': user_reg}
                    return render(request, 'accounts/Sign_up.html', context)
        return render(request, 'accounts/Sign_up.html', {'reg': reg})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            if request.POST.get('login') == "admin":
                username = request.POST.get('admin_name')
                password = request.POST.get('admin_password')
                user = authenticate(request, username=username, password=password)

                if user is not None and user.is_staff == 1:
                    request.session['Admin_Check'] = "ADMIN"
                    login(request, user)
                    return redirect('index')

                else:
                    messages.info(request, 'Username OR password is incorrect')
                    return render(request, 'accounts/Sign_up.html')
            elif request.POST.get('login') == "user":
                username = request.POST.get('username')
                print(username)
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password, is_staff=0)

                if user is not None and user.is_superuser == 1:
                    login(request, user)
                    return redirect('index')

                else:
                    user_log = "yes"
                    messages.info(request, 'Username OR password is incorrect')
                    return render(request, 'accounts/Sign_up.html', {'user_log': user_log})
        else:
            print("yaya")
            context = {}
            return render(request, 'accounts/Sign_up.html', context)


def logoutUser(request):
    logout(request)

    return redirect('login')


@login_required(login_url='login')
def index(request):
    if request:
        print("okokokoko")
        emp_count = new_emp_reg.objects.count()
        cli_count = New_Customer_Reg.objects.count()
        file_count = MANAGE_FILES.objects.count()
        notice_count = NOTICE_BOARD.objects.filter(STATUS="Published").count()
        holiday_count = HOLIDAYS.objects.filter(STATUS="Published").count()
        data = NOTICE_BOARD.objects.all()
        holiday = HOLIDAYS.objects.all()
        notice_data_list = []
        holi_data_list = []
        notice_list = "not_null"
        holidays_list = "not_null"
        count = 0
        for details in data:
            if details.STATUS == "Published":
                count += 1

                class details_class:
                    ID = count
                    TITLE = details.TITLE
                    DESCRIPTION = details.DESCRIPTION

                notice_data_list.append(details_class)
        count = 0
        for details in holiday:
            if details.STATUS == "Published":
                count += 1

                class details_class:
                    ID = count
                    HOLIDAY_NAME = details.HOLIDAY_NAME
                    HOLIDAY_DATE = details.HOLIDAY_DATE
                    DESCRIPTION = details.DESCRIPTION

                holi_data_list.append(details_class)
        if not notice_data_list:
            notice_list = "null"
        if not holi_data_list:
            holidays_list = "null"
        value = {
            'emp_count': emp_count,
            'cli_count': cli_count,
            'holidays_list': holidays_list,
            'notice_list': notice_list,
            'file_count': file_count,
            'notice_count': notice_count,
            'holiday_count': holiday_count,
            'notice_data_list': notice_data_list,
            'holi_data_list': holi_data_list,
        }
        return render(request, 'index.html', value)


@login_required(login_url='login')
def new_employee_register(request):
    if request.method == 'POST':
        form_valid_check = {"client": "CLIENT", "country": "COUNTRY", "company_state": "STATE",
                            "company_district": "DISTRICT", "branch": "BRANCH", "area": "AREA", "unit": "UNIT",
                            "doj": "DATE OF JOIN", "employee_name": "EMPLOYER NAME", "designation": "DESIGNATION",
                            "marital_status": "MARITAL STATUS", "wife_husband": "WIFE/HUSBAND NAME",
                            "father_name": "FATHER NAME", "mother_name": "MOTHER NAME", "gender": "GENDER",
                            "higher_edu": "HIGHEST EDUCATION", "aadhar_no": "AADHAR NO", "dob": "DATE OF BIRTH",
                            "pan_no": "PAN NO", "uan_no": "UAN NO", "pf_no": "PF NO", "id_card_no": "ID CARD NO",
                            "esi_no": "ESI NO", "bank_account_no": "ACCOUNT NO", "ifsc_code": "IFSC CODE",
                            "bank_name": "BANK NAME", "nationality": "NATIONALITY", "blood_group": "BLOOD GROUP",
                            "per_address": "PERMANENT ADDRESS", "address": "CURRENT ADDRESS", "email_id": "EMAIL ID",
                            "mobile_no": "MOBILE NO", "contact_no": "CONTACT NO", "basic": "BASIC",
                            "dea_all": "DEARANCE ALLOWANCES", "hra": "HOUSE RENT ALLOWANCES"}
        check_valid = []
        print(request.POST.get('fix_sal'), "DESIGNATION")
        for key in form_valid_check:
            if not request.POST.get(key):
                check_valid.append(form_valid_check[key] + " VALUE IS NONE PLZ ENTER PROPERLY")

        DATE = datetime.now().strftime("%Y-%m-%d")
        TIME = datetime.now().strftime("%H:%m")
        print(request.POST.get('per_address'), "yes or")
        if not check_valid:
            try:
                aadthar = EMP_PERSONAL_DETAILS.objects.get(PAN_NO=request.POST.get('pan_no'))
                request.session['New_Employee_Req'] = "Already Exist This Employee  : "
                request.session['New_Employee_Code'] = " "
            except EMP_PERSONAL_DETAILS.DoesNotExist:
                try:
                    last_id = new_emp_reg.objects.latest('ID')
                    increse = int(last_id.EMP_CODE) + 1
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
                FIXED_SALARY = request.POST.get('fix_sal')
                BASIC = request.POST.get('basic')
                DEARANCE_ALLOWANCES = request.POST.get('dea_all')
                SPECIAL_ALLOWANCES = request.POST.get('spa')
                HOUSE_RENT_ALLOWANCES = request.POST.get('hra')
                CONVEYANCE = request.POST.get('con')
                OTHER_ALLOWANCES = request.POST.get('ota')
                OVERTIME_AMOUNT = request.POST.get('ot')
                SITE_ALLOWANCES = request.POST.get('sta')
                SHIFT_ALLOWANCES_AMOUNT = request.POST.get('e_sf_pay')
                INCENTIVE = request.POST.get('inc')
                LEAVE_TRAVEL_ALLOWANCES = request.POST.get('lta')
                MEDICAL_ALLOWANCES = request.POST.get('med_a')
                CHILD_EDUCATIONS_ALLOWANCES = request.POST.get('cea')
                ATTENDANCE_BONUS = request.POST.get('att_bo')
                ATTENDANCE_INCENTIVE = request.POST.get('att_in')
                EXTRA_BOUNS = request.POST.get('extra_bo')
                MONTHLY_LEAVE_WAGES = request.POST.get('mon_le_wa')
                PF = request.POST.get('mon_pf')
                ESIC = request.POST.get('mon_esic')
                RELIVER_DUTY_WAGES = request.POST.get('re_du_wa')
                ARREARS_WAGES = request.POST.get('arr_wa')
                PROFESSIONAL_TAX = request.POST.get('pro_tax')
                LABOUR_WELFARE_FUND = request.POST.get('la_we_fu')
                INCOME_TAX = request.POST.get('income_tax')
                LOAN = request.POST.get('loan')
                SALARY_ADVANCE = request.POST.get('salary_adv')
                OTHER_DEDUCTION = request.POST.get('other_dec')
                UNIFORM_DEDUCTION = request.POST.get('uni_dec')
                if not request.POST.get('fix_sal'):
                    FIXED_SALARY = 0
                if not request.POST.get('basic'):
                    BASIC = 0
                if not request.POST.get('dea_all'):
                    DEARANCE_ALLOWANCES = 0
                if not request.POST.get('spa'):
                    SPECIAL_ALLOWANCES = 0
                if not request.POST.get('hra'):
                    HOUSE_RENT_ALLOWANCES = 0
                if not request.POST.get('con'):
                    CONVEYANCE = 0
                if not request.POST.get('ota'):
                    OTHER_ALLOWANCES = 0
                if not request.POST.get('ot'):
                    OVERTIME_AMOUNT = 0
                if not request.POST.get('sta'):
                    SITE_ALLOWANCES = 0
                if not request.POST.get('e_sf_pay'):
                    SHIFT_ALLOWANCES_AMOUNT = 0
                if not request.POST.get('inc'):
                    INCENTIVE = 0
                if not request.POST.get('lta'):
                    LEAVE_TRAVEL_ALLOWANCES = 0
                if not request.POST.get('med_a'):
                    MEDICAL_ALLOWANCES = 0
                if not request.POST.get('cea'):
                    CHILD_EDUCATIONS_ALLOWANCES = 0
                if not request.POST.get('att_bo'):
                    ATTENDANCE_BONUS = 0
                if not request.POST.get('att_in'):
                    ATTENDANCE_INCENTIVE = 0
                if not request.POST.get('extra_bo'):
                    EXTRA_BOUNS = 0
                if not request.POST.get('mon_le_wa'):
                    MONTHLY_LEAVE_WAGES = 0
                if not request.POST.get('re_du_wa'):
                    RELIVER_DUTY_WAGES = 0
                if not request.POST.get('arr_wa'):
                    ARREARS_WAGES = 0
                if not request.POST.get('pro_tax'):
                    PROFESSIONAL_TAX = 0
                if not request.POST.get('la_we_fu'):
                    LABOUR_WELFARE_FUND = 0
                if not request.POST.get('income_tax'):
                    INCOME_TAX = 0
                if not request.POST.get('loan'):
                    LOAN = 0
                if not request.POST.get('salary_adv'):
                    SALARY_ADVANCE = 0
                if not request.POST.get('other_dec'):
                    OTHER_DEDUCTION = 0
                if not request.POST.get('uni_dec'):
                    UNIFORM_DEDUCTION = 0

                new_emp_register = new_emp_reg(
                    EMP_NAME=request.POST.get('employee_name'),
                    EMP_CODE=new_id,
                    DOB=request.POST.get('dob'),
                    GENDER=request.POST.get('gender'),
                    REG_DATE=DATE,
                    REG_TIME=TIME,
                    SALUTATION=request.POST.get('salutation'),
                    MARITAL_STATUS=request.POST.get('marital_status'),
                    MOBILE_NO=request.POST.get('contact_no'),
                    AGE=request.POST.get('age'),
                    EXPERIANCE=request.POST.get('experiance'),
                )
                new_emp_register.save()
                emp_id = new_emp_register.ID

                emp_company_reg = EMP_COMPANY_DETAILS(
                    EMP_CODE=new_id,
                    EMP_LINK=new_emp_register,
                    COUNTRY=request.POST.get('country'),
                    STATE=request.POST.get('company_state'),
                    DISTRICT=request.POST.get('company_district'),
                    BRANCH=request.POST.get('branch'),
                    AREA=request.POST.get('area'),
                    CLIENT=request.POST.get('client'),
                    UNIT=request.POST.get('unit'),
                    DATE_OF_JOIN=request.POST.get('doj'),
                    BIO_DATE_SUB_DATE=request.POST.get('bdsb'),
                    DESIGNATION=request.POST.get('designation'),
                    CATEGORY=request.POST.get('category'),
                    ISSUE_DATE=request.POST.get('issue_date'),
                    VAILD_DATE=request.POST.get('valid_date')
                )
                emp_company_reg.save()

                emp_per_details = EMP_PERSONAL_DETAILS(
                    EMP_CODE=new_id,
                    EMP_LINK=emp_company_reg,
                    WIFE_HUSBAND_NAME=request.POST.get('wife_husband'),
                    FATHER_NAME=request.POST.get('father_name'),
                    MOTHER_NAME=request.POST.get('mother_name'),
                    HIGHEST_EDUCATION=request.POST.get('higher_edu'),
                    BIRTH_PLACE=request.POST.get('birth_place'),
                    PAN_NO=request.POST.get('pan_no'),
                    PF_NO=request.POST.get('pf_no'),
                    ESI_NO=request.POST.get('esi_no'),
                    AADHAR_NO=request.POST.get('aadhar_no'),
                    UAN_NO=request.POST.get('uan_no'),
                    ID_CARD_NO=request.POST.get('id_card_no'),
                    NATIONALITY=request.POST.get('nationality'),
                    BLOOD_GROUP=request.POST.get('blood_group'),
                    SHOE_SIZE=request.POST.get('shoe_size'),
                    WAIST=request.POST.get('waist'),
                    HEIGHT=request.POST.get('height'),
                    WEIGHT=request.POST.get('weight'),
                    CHEST=request.POST.get('chest'),
                    T_SHIRT_SIZE=request.POST.get('t_shirt'),
                    THOUSER_SIZE=request.POST.get('thouser_size')
                )
                emp_per_details.save()
                if request.POST.get('permanet_address') == "on":

                    PER_ADDRESS = request.POST.get('address')
                    PER_STREET = request.POST.get('street')
                    PER_DISTRICT = request.POST.get('district')
                    PER_PINCODE = request.POST.get('pin_code')
                    PER_DURATION = request.POST.get('duration')
                    PER_STATE = request.POST.get('state')
                else:
                    PER_ADDRESS = request.POST.get('per_address')
                    PER_STREET = request.POST.get('per_street')
                    PER_DISTRICT = request.POST.get('per_district')
                    PER_PINCODE = request.POST.get('per_pin_code')
                    PER_DURATION = request.POST.get('per_duration')
                    PER_STATE = request.POST.get('per_state')

                emp_comm_details = EMP_COMMUNICATION_DETAILS(
                    EMP_CODE=new_id,
                    EMP_LINK=emp_per_details,
                    ADDRESS=request.POST.get('address'),
                    STREET=request.POST.get('street'),
                    DISTRICT=request.POST.get('district'),
                    PINCODE=request.POST.get('pin_code'),
                    TELEPHONE=request.POST.get('telephone'),
                    MOBILE_NO=request.POST.get('mobile_no'),
                    EMAIL_ID=request.POST.get('email_id'),
                    DURATION=request.POST.get('duration'),
                    STATE=request.POST.get('state'),
                    PER_ADDRESS=PER_ADDRESS,
                    PER_STREET=PER_STREET,
                    PER_DISTRICT=PER_DISTRICT,
                    PER_PINCODE=PER_PINCODE,
                    PER_DURATION=PER_DURATION,
                    PER_STATE=PER_STATE
                )
                emp_comm_details.save()

                emp_bank_details = EMP_BANK_DETAILS(
                    EMP_CODE=new_id,
                    EMP_LINK=emp_comm_details,
                    ACCOUNT_NO=request.POST.get('bank_account_no'),
                    BANK_NAME=request.POST.get('bank_name'),
                    IFSC_CODE=request.POST.get('ifsc_code'),
                    BRANCH=request.POST.get('bank_branch'),
                    PAYMENT_MODE=request.POST.get('payment_mode'),
                    PASSBOOK_NAME=request.POST.get('passbook_name'),
                    JOIN_ACC_NO=request.POST.get('join_acc_no'),
                    JOIN_ACC_NAME=request.POST.get('join_acc_bank_name'),
                    JOIN_ACC_BRANCH_NAME=request.POST.get('join_acc_name'),
                    JOIN_ACC_BANK_NAME=request.POST.get('join_acc_br_name')

                )
                emp_bank_details.save()

                emp_salary_details = salary_details(
                    EMP_CODE=new_id,
                    EMP_LINK=emp_bank_details,
                    FIXED_SALARY=FIXED_SALARY,
                    MONTH_SALARY=FIXED_SALARY,
                    BASIC=BASIC,
                    DEARANCE_ALLOWANCES=DEARANCE_ALLOWANCES,
                    SPECIAL_ALLOWANCES=SPECIAL_ALLOWANCES,
                    HOUSE_RENT_ALLOWANCES=HOUSE_RENT_ALLOWANCES,
                    CONVEYANCE=CONVEYANCE,
                    OTHER_ALLOWANCES=OTHER_ALLOWANCES,
                    OVERTIME_AMOUNT=OVERTIME_AMOUNT,
                    SITE_ALLOWANCES=SITE_ALLOWANCES,
                    SHIFT_ALLOWANCES_AMOUNT=SHIFT_ALLOWANCES_AMOUNT,
                    INCENTIVE=INCENTIVE,
                    LEAVE_TRAVEL_ALLOWANCES=LEAVE_TRAVEL_ALLOWANCES,
                    MEDICAL_ALLOWANCES=MEDICAL_ALLOWANCES,
                    CHILD_EDUCATIONS_ALLOWANCES=CHILD_EDUCATIONS_ALLOWANCES,
                    ATTENDANCE_BONUS=ATTENDANCE_BONUS,
                    ATTENDANCE_INCENTIVE=ATTENDANCE_INCENTIVE,
                    MONTHLY_BOUNS=0,
                    EXTRA_BOUNS=EXTRA_BOUNS,
                    MONTHLY_LEAVE_WAGES=MONTHLY_LEAVE_WAGES,
                    ESIC=0,
                    RELIVER_DUTY_WAGES=RELIVER_DUTY_WAGES,
                    ARREARS_WAGES=ARREARS_WAGES,
                    PROFESSIONAL_TAX=0,
                    LABOUR_WELFARE_FUND=0,
                    INCOME_TAX=INCOME_TAX,
                    LOAN=LOAN,
                    SALARY_ADVANCE=SALARY_ADVANCE,
                    OTHER_DEDUCTION=OTHER_DEDUCTION,
                    UNIFORM_DEDUCTION=UNIFORM_DEDUCTION,
                    TOTAL_EARN=0,
                    TOTAL_DEDUCATION=0,
                    NET_PAY=0,
                    PROVIDENT_FUND=0,
                    SALARY_UPDATE_DATE="NO UPDATED",
                    NAMINE_E_NAME=request.POST.get('namine_name'),
                    NAMINE_E_RELATIONS=request.POST.get('namine_relation'),
                )
                emp_salary_details.save()
                emp_daily_attendance = EMP_DAILY_ATTENDANCE_UPDATED(
                    EMP_CODE=new_id,
                    EMP_NAME=request.POST.get('employee_name'),
                    DESIGNATION=request.POST.get('designation'),
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

                    VERFICATION_NO=request.POST.get('verification_no'),
                    VERFICATION_DATE=request.POST.get('verification_date'),
                    CRIMINOLOGY=request.POST.get('criminology'),
                    PV_SEND_DATE=request.POST.get('pv_send_date'),
                    PV_RETURN_DATE=request.POST.get('pv_return_date'),
                    NAME_OF_POLICE_THANA=request.POST.get('name_of_police_thana'),
                    IDENTITY_SIGN=request.POST.get('identity_sign'),
                    PV_VALID_UPTO=request.POST.get('pv_valid_date'),
                    REMARK_BY_THANA=request.POST.get('remark_by_thana'),

                )
                request.session['New_Employee_Req'] = "Successfully Created Employee  : " + request.POST.get(
                    'employee_name')
                request.session['New_Employee_Code'] = " Employee Code : ", new_id

            return redirect(reverse('New_Employee_Reg'))  # We redirect to the same view
            # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
        else:
            newlist = []
            client = CLIENT_DETAILS.objects.all()
            for i in range(len(client)):
                variable = client[i].CLIENT
                print(variable)
                if variable not in newlist:
                    newlist.append(variable)
            print(newlist)
            designation_list = DESIGNATION_LIST.objects.filter(STATUS="Published")
            bank_list = BANK_LIST.objects.all()
            form = request.POST
            stu = {
                "error": check_valid,
                'client': newlist,
                'designation_list': designation_list,
                'bank_list': bank_list,
                "form": form,
            }
            return render(request, 'new_employee_reg.html', stu)

    else:
        session_emp_name = ""
        session_emp_code = ""
    newlist = []
    client = CLIENT_DETAILS.objects.all()
    for i in range(len(client)):
        variable = client[i].CLIENT
        print(variable)
        if variable not in newlist:
            newlist.append(variable)
    print(newlist)
    designation_list = DESIGNATION_LIST.objects.filter(STATUS="Published")
    bank_list = BANK_LIST.objects.all()
    if 'New_Employee_Req' not in request.session:
        value = {
            'client': newlist,
            'designation_list': designation_list,
            'bank_list': bank_list,
        }
        return render(request, 'new_employee_reg.html', value)
    else:

        session_emp_name = request.session['New_Employee_Req']
        session_emp_code = request.session['New_Employee_Code']

        del request.session["New_Employee_Req"]
        del request.session["New_Employee_Code"]
        request.session.modified = True

        value = {
            'client': newlist,
            'designation_list': designation_list,
            'bank_list': bank_list,
            'session_emp_name': session_emp_name,
            'session_emp_code': session_emp_code
        }
        return render(request, 'new_employee_reg.html', value)


@login_required(login_url='login')
def new_customer_register(request):
    if request.method == 'POST':
        DATE = datetime.now().strftime("%Y-%m-%d")
        TIME = datetime.now().strftime("%H:%m")
        try:
            last_id = New_Customer_Reg.objects.latest('ID')
            print(type(last_id.CLIENT_CODE), "LAST ID try")
            increse = int(last_id.CLIENT_CODE) + 1
            print(increse)
            if increse < 10:
                new_id = "000" + str(increse)
            elif increse >= 10 and increse < 100:
                new_id = "00" + str(increse)
            elif increse >= 100 and increse < 1000:
                new_id = "0" + str(increse)
            elif increse >= 1000:
                new_id = str(increse)
        except New_Customer_Reg.DoesNotExist:
            new_id = "0001"
        new_customer_register = New_Customer_Reg(
            CLIENT_CODE=new_id,
            CLIENT_NAME=request.POST.get('client_name'),
            EMAIL=request.POST.get('client_email'),
            DOB=request.POST.get('doj'),
            CONTACT_NO=request.POST.get('client_ph'),
            WEB=request.POST.get('web'),
            GENTER=request.POST.get('gender'),
            EMERGENCY_CONTACT_NO=request.POST.get('emg_ph'),
            ADDRESS=request.POST.get('address'),
            REG_DATE=DATE,
            REG_TIME=TIME,
            CLIENT_TYPE=request.POST.get('client_type'),
        )
        new_customer_register.save()
        request.session['New_Client_Req'] = "Successfully Created Client  : " + request.POST.get(
            'client_name')
        request.session['New_Client_Code'] = " Employee Code : ", new_id

        return redirect(reverse('New_Customer_Reg'))  # We redirect to the same view

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            data = CLIENT_TYPE.objects.filter(STATUS="Published")
            return render(request, 'new_customer.html', {'data': data})
        else:
            data = CLIENT_TYPE.objects.filter(STATUS="Published")
            session_client_name = request.session['New_Client_Req']
            session_client_code = request.session['New_Client_Code']

            del request.session["New_Client_Req"]
            del request.session["New_Client_Code"]
            request.session.modified = True

            return render(request, 'new_customer.html',
                          {'session_client_name': session_client_name, 'session_client_code': session_client_code,
                           'data': data})


@login_required(login_url='login')
def salary_sheet(request):
    if request.method == 'POST':
        client = request.POST.get('client')
        country = request.POST.get('country')
        state = request.POST.get('company_state')
        district = request.POST.get('company_district')
        branch = request.POST.get('branch')
        area = request.POST.get('area')
        unit = request.POST.get('unit')

        data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                             'NEW_EMP').filter(EMP_COMPANY__CLIENT=client,
                                                                               EMP_COMPANY__COUNTRY=country,
                                                                               EMP_COMPANY__STATE=state,
                                                                               EMP_COMPANY__DISTRICT=district,
                                                                               EMP_COMPANY__BRANCH=branch,
                                                                               EMP_COMPANY__AREA=area,
                                                                               EMP_COMPANY__UNIT=unit)
        address = CLIENT_DETAILS.objects.get(CLIENT=client,
                                             COUNTRY_NAME=country,
                                             STATE_NAME=state,
                                             DISTRICT_NAME=district,
                                             BRANCH_NAME=branch,
                                             AREA_NAME=area,
                                             UNIT=unit)
        print(address.ADDRESS, "ADDRESS")
        count = 0
        em_mon_report = []
        Total_salary = 0
        total_deducation = 0
        total_net_pay = 0
        for details in data:
            emp_code = details.NEW_EMP.EMP_CODE
            emp_name = details.NEW_EMP.EMP_NAME
            desgn = details.EMP_COMPANY.DESIGNATION
            print(emp_code)
            data1 = EMP_SALARY_MAINTAINS.objects.filter(SALARY_UPDATE_DATE=request.POST.get('date_month'),
                                                        EMP_CODE=emp_code)
            for sal in data1:
                count += 1
                Total_salary = Total_salary + float(sal.TOTAL_EARN)
                total_deducation = total_deducation + float(sal.TOTAL_DEDUCATION)
                total_net_pay = "{:.2f}".format(Total_salary - total_deducation)

                class details_class:
                    id = count
                    EMP_NAME = emp_name
                    EMP_CODE = emp_code
                    DESIGNATION = desgn
                    TOTAL_EARN = sal.TOTAL_EARN
                    TOTAL_DEDUCATION = sal.TOTAL_DEDUCATION
                    NET_PAY = sal.NET_PAY
                    SALARY_UPDATE_DATE = sal.SALARY_UPDATE_DATE

                em_mon_report.append(details_class)

        value = {
            'data': em_mon_report,
            'month_sal': request.POST.get('date_month'),
            'total_salry': Total_salary,
            'total_deducation': total_deducation,
            'total_net_pay': total_net_pay,
            'client': client,
            'address': address.ADDRESS,
            'state': state,
            'district': district,

        }
        return render(request, 'salary_sheet_view.html', value)
    else:
        newlist = []
        client = CLIENT_DETAILS.objects.all()
        for i in range(len(client)):
            variable = client[i].CLIENT
            print(variable)
            if variable not in newlist:
                newlist.append(variable)
        return render(request, 'salary_sheet.html', {'client': newlist})


@login_required(login_url='login')
def attendance_report(request):
    if request.method == 'POST':

        data = MONTHLY_ATTENDANCE_DETAILS.objects.filter(MONTH_YEAR=request.POST.get(
            'date_month'))
        if not data:
            error_messege = "data_is_empty"
            return render(request, 'monthly_attendance_details.html',
                          {'data': error_messege, 'month_sal': request.POST.get('date_month')})
        else:
            return render(request, 'monthly_attendance_details.html',
                          {'data': data, 'month_sal': request.POST.get('date_month')})
    else:
        return render(request, 'select_month_attendance.html')


@login_required(login_url='login')
def month_attendance_report(request):
    if request.method == "POST":
        client_list = []
        report_array = []
        country_list = []
        client = CLIENT_DETAILS.objects.all()
        for i in range(len(client)):
            variable = client[i].CLIENT
            print(variable)
            if variable not in client_list:
                client_list.append(variable)
        filter_client = request.POST.get('client')
        result_set = []
        filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=filter_client)
        for client_details in filter_client_list:
            result_set.append(client_details)

        for i in range(len(result_set)):
            country = result_set[i].COUNTRY_NAME
            if country not in country_list:
                country_list.append(country)
        filter_value = "no"
        data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                             'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client)

        for emp_details in data:
            EMP_CODE = emp_details.NEW_EMP.EMP_CODE
            print(EMP_CODE)
            employer_details = EMP_SALARY_MAINTAINS.objects.filter(EMP_CODE=EMP_CODE,
                                                                   SALARY_UPDATE_DATE=request.POST.get('date_month'))
            for data1 in employer_details:
                filter_value = "yes"
                print(data1.EMP_CODE)

                class details_class:
                    emp_code = data1.EMP_CODE
                    Name = emp_details.NEW_EMP.EMP_NAME
                    design = emp_details.EMP_COMPANY.DESIGNATION
                    WORKING_DAYS = data1.DAYS_PRESENT
                    OVER_TIME = data1.OVERTIME_HRS

                report_array.append(details_class)

        dummy_value = request.POST.get('client') + "~" + request.POST.get('date_month')
        client_name = request.POST.get('client')
        date_month = request.POST.get('date_month')
        # wage_de = Form_B_Obj(client, unit, month, year)
        value = {
            'data': report_array,
            'client': client_list,
            'country_list': country_list,
            'filter_value': filter_value,
            'dummy_value': dummy_value,
            'client_name': client_name,
            'date_month': date_month,
        }

        return render(request, 'month_attendance_report.html', value)

    else:
        if request.GET.get('client') is None:
            client_list = []
            client = CLIENT_DETAILS.objects.all()
            for i in range(len(client)):
                variable = client[i].CLIENT
                print(variable)
                if variable not in client_list:
                    client_list.append(variable)
            value = {
                'client': client_list,
            }
        else:
            get_value = request.GET.get('client').split('~')
            client_list = []
            report_array = []
            country_list = []
            client = CLIENT_DETAILS.objects.all()
            for i in range(len(client)):
                variable = client[i].CLIENT
                print(variable)
                if variable not in client_list:
                    client_list.append(variable)
            result_set = []
            filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=get_value[0])
            for client_details in filter_client_list:
                result_set.append(client_details)

            for i in range(len(result_set)):
                country = result_set[i].COUNTRY_NAME
                if country not in country_list:
                    country_list.append(country)
            form = request.POST
            filter_value = "no"
            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=get_value[0])

            for emp_details in data:
                EMP_CODE = emp_details.NEW_EMP.EMP_CODE
                print(EMP_CODE)
                employer_details = EMP_SALARY_MAINTAINS.objects.filter(EMP_CODE=EMP_CODE,
                                                                       SALARY_UPDATE_DATE=get_value[1])
                for data1 in employer_details:
                    filter_value = "yes"
                    print(data1.FIXED_SALARY, "dd")

                    class details_class:
                        emp_code = data1.EMP_CODE
                        Name = emp_details.NEW_EMP.EMP_NAME
                        design = emp_details.EMP_COMPANY.DESIGNATION
                        WORKING_DAYS = data1.DAYS_PRESENT
                        OVER_TIME = data1.OVERTIME_HRS

                    report_array.append(details_class)

            dummy_value = get_value[0] + "~" + get_value[1]
            client_name = get_value[0]
            date_month = get_value[1]
            # wage_de = Form_B_Obj(client, unit, month, year)
            value = {
                'data': report_array,
                'client': client_list,
                'country_list': country_list,
                'filter_value': filter_value,
                'dummy_value': dummy_value,
                'client_name': client_name,
                'date_month': date_month,
            }
        return render(request, 'month_attendance_report.html', value)


@login_required(login_url='login')
def Filter_month_attendance_report(request):
    if request.method == "POST":
        client_list = []
        country_list = []
        report_array = []
        filter_client = request.POST.get('client_name')
        date_month = request.POST.get('date_month')
        print(filter_client[0], "dyjhgdas")
        client = CLIENT_DETAILS.objects.all()
        form_a_filter = ""
        for i in range(len(client)):
            variable = client[i].CLIENT
            print(variable, "variable")
            if variable not in client_list:
                client_list.append(variable)
        filter_value = "yes"
        result_set = []
        filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=filter_client)
        for client_details in filter_client_list:
            result_set.append(client_details)

        for i in range(len(result_set)):
            country = result_set[i].COUNTRY_NAME
            if country not in country_list:
                country_list.append(country)
        if request.POST.get('submit') == "Country":
            form_a_filter = "Country" + "~" + filter_client + "~" + date_month + "~" + request.POST.get('country_name')
            country_name = request.POST.get('country_name')
            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name)
        elif request.POST.get('submit') == "State":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            form_a_filter = "State" + "~" + filter_client + "~" + date_month + "~" + country_name + "~" + state_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name)
        elif request.POST.get('submit') == "District":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            form_a_filter = "District" + "~" + filter_client + "~" + date_month + "~" + country_name + "~" + state_name + "~" + district_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name)
        elif request.POST.get('submit') == "Branch":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            branch_name = request.POST.get('branch_name')
            form_a_filter = "Branch" + "~" + filter_client + "~" + date_month + "~" + country_name + "~" + state_name + "~" + district_name + "~" + branch_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name,
                                                                                   EMP_COMPANY__BRANCH=branch_name)
        elif request.POST.get('submit') == "Area":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            branch_name = request.POST.get('branch_name')
            area_name = request.POST.get('area_name')
            form_a_filter = "Branch" + "~" + filter_client + "~" + date_month + "~" + country_name + "~" + state_name + "~" + district_name + "~" + branch_name + "~" + area_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name,
                                                                                   EMP_COMPANY__BRANCH=branch_name,
                                                                                   EMP_COMPANY__AREA=area_name)
        elif request.POST.get('submit') == "Unit":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            branch_name = request.POST.get('branch_name')
            area_name = request.POST.get('area_name')
            unit = request.POST.get('unit_name')
            form_a_filter = "Unit" + "~" + filter_client + "~" + date_month + "~" + country_name + "~" + state_name + "~" + district_name + "~" + branch_name + "~" + area_name + "~" + unit

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name,
                                                                                   EMP_COMPANY__BRANCH=branch_name,
                                                                                   EMP_COMPANY__AREA=area_name,
                                                                                   EMP_COMPANY__UNIT=unit)
        for emp_details in data:
            EMP_CODE = emp_details.NEW_EMP.EMP_CODE
            employer_details = EMP_SALARY_MAINTAINS.objects.filter(EMP_CODE=EMP_CODE,
                                                                   SALARY_UPDATE_DATE=date_month)
            for data1 in employer_details:
                class details_class:
                    emp_code = data1.EMP_CODE
                    Name = emp_details.NEW_EMP.EMP_NAME
                    design = emp_details.EMP_COMPANY.DESIGNATION
                    WORKING_DAYS = data1.DAYS_PRESENT
                    OVER_TIME = data1.OVERTIME_HRS

                report_array.append(details_class)
        value = {
            'data': report_array,
            'client': client_list,
            'error_message': data,
            'country_list': country_list,
            'filter_value': filter_value,
            'client_name': filter_client,
            'date_month': date_month,
            'form_a_filter': form_a_filter,
        }
        return render(request, 'month_attendance_report.html', value)
    else:
        if request.GET.get('client') is None:
            return redirect(reverse('Month_Attendance_Report'))
        else:
            get_value = request.GET.get('client').split('~')
            client_list = []
            country_list = []
            report_array = []
            filter_client = get_value[1]
            client = CLIENT_DETAILS.objects.all()
            form_a_filter = ""
            for i in range(len(client)):
                variable = client[i].CLIENT
                if variable not in client_list:
                    client_list.append(variable)
            filter_value = "yes"
            result_set = []
            filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=filter_client)
            for client_details in filter_client_list:
                result_set.append(client_details)

            for i in range(len(result_set)):
                country = result_set[i].COUNTRY_NAME
                if country not in country_list:
                    country_list.append(country)
            if get_value[0] == "Country":
                form_a_filter = "Country" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[3])
            elif get_value[0] == "State":
                form_a_filter = "State" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + \
                                get_value[4]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[3],
                    EMP_COMPANY__STATE=get_value[4])
            elif get_value[0] == "District":
                form_a_filter = "District" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + \
                                get_value[4] + "~" + get_value[5]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[3],
                    EMP_COMPANY__STATE=get_value[4],
                    EMP_COMPANY__DISTRICT=get_value[5])
            elif get_value[0] == "Branch":
                form_a_filter = "Branch" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + \
                                get_value[4] + "~" + get_value[5] + "~" + get_value[6]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[3],
                    EMP_COMPANY__STATE=get_value[4],
                    EMP_COMPANY__DISTRICT=get_value[5],
                    EMP_COMPANY__BRANCH=get_value[6])
            elif get_value[0] == "Area":
                form_a_filter = "Area" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + get_value[
                    4] + "~" + get_value[5] + "~" + get_value[6] + "~" + get_value[7]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[3],
                    EMP_COMPANY__STATE=get_value[4],
                    EMP_COMPANY__DISTRICT=get_value[5],
                    EMP_COMPANY__BRANCH=get_value[6],
                    EMP_COMPANY__AREA=get_value[7])
            elif get_value[0] == "Unit":
                form_a_filter = "Unit" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + get_value[
                    4] + "~" + get_value[5] + "~" + get_value[6] + "~" + get_value[7] + "~" + get_value[8]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[3],
                    EMP_COMPANY__STATE=get_value[4],
                    EMP_COMPANY__DISTRICT=get_value[5],
                    EMP_COMPANY__BRANCH=get_value[6],
                    EMP_COMPANY__AREA=get_value[7],
                    EMP_COMPANY__UNIT=get_value[8])
            for emp_details in data:
                EMP_CODE = emp_details.NEW_EMP.EMP_CODE
                employer_details = EMP_SALARY_MAINTAINS.objects.filter(EMP_CODE=EMP_CODE,
                                                                       SALARY_UPDATE_DATE=get_value[2])
                for data1 in employer_details:
                    class details_class:
                        emp_code = data1.EMP_CODE
                        Name = emp_details.NEW_EMP.EMP_NAME
                        design = emp_details.EMP_COMPANY.DESIGNATION
                        WORKING_DAYS = data1.DAYS_PRESENT
                        OVER_TIME = data1.OVERTIME_HRS

                    report_array.append(details_class)
            value = {
                'data': report_array,
                'client': client_list,
                'error_message': data,
                'country_list': country_list,
                'filter_value': filter_value,
                'client_name': filter_client,
                'date_month': get_value[2],
                'form_a_filter': form_a_filter,
            }
            return render(request, 'month_attendance_report.html', value)


@login_required(login_url='login')
def employee_list(request):
    data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMPANY', 'EMP_SAL').all()
    em_mon_report = []
    count = 0
    # The mail addresses and password
    # sender_address = 'muthuheroku2001@gmail.com'
    # sender_pass = 'ixdxriqtcplwjysk'
    # receiver_address = 'ms.kmd007@gmail.com'
    # mail_content = '''Hello,
    # This is a test mail.
    # In this mail we are sending some attachments.
    # The mail is sent using Python SMTP library.
    # Thank You
    # '''
    # Setup the MIME
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = 'A test mail sent by Python. It has an attachment.'
    # The body and the attachments for the mail
    # message.attach(MIMEText(mail_content, 'plain'))
    # attach_file_name = 'templates/media/FOLDER A/ExampleFile.pdf'
    # attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    # payload = MIMEBase('application', 'pdf',Name=attach_file_name)
    # payload.set_payload((attach_file).read())
    # encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    # payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    # message.attach(payload)
    # Create SMTP session for sending the mail
    # session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    # session.starttls()  # enable security
    # session.login(sender_address, sender_pass)  # login with mail_id and password
    # text = message.as_string()
    # session.sendmail(sender_address, receiver_address, text)
    # session.quit()
    # server = smtplib.SMTP('smtp.gmail.com', 587)

    # server.starttls()

    # server.login('', '')

    # server.sendmail('muthuheroku2001@gmail.com', 'ms.kmd007@gmail.com', 'python code')

    print("success")
    if not data:
        error_messege = "data_is_empty"
        return render(request, 'emp_list.html', {'data': error_messege, })
    else:
        for details in data:
            count += 1

            class details_class:
                id = count
                EMP_NAME = details.NEW_EMP.EMP_NAME
                EMP_CODE = details.NEW_EMP.EMP_CODE
                DESIGNATION = details.EMP_COMPANY.DESIGNATION
                REG_DATE = details.NEW_EMP.REG_DATE
                MOBILE_NO = details.NEW_EMP.MOBILE_NO

            em_mon_report.append(details_class)
        return render(request, 'emp_list.html', {'data': em_mon_report})


@login_required(login_url='login')
def daily_att_list(request):
    if request.method == 'POST':
        DATE = datetime.now().strftime("%B-%Y")

        EMP_NAME = request.POST.get('emp_name')
        EMP_CODE = request.POST.get('emp_code')
        DESIGNATION = request.POST.get('emp_design')

        data = EMP_DAILY_ATTENDANCE_LIST.objects.filter(ATTENDANCE_MONTH=request.POST.get('date_month'),
                                                        EMP_CODE=EMP_CODE)
        em_mon_report = []
        count = 0
        total_present = 0
        total_absent = 0
        total_leave = 0
        if not data:
            error_messege = "data_is_empty"
            return render(request, 'emp_daily_attendance.html',
                          {'data': error_messege, 'month_att': request.POST.get('date_month'),
                           'emp_name': EMP_NAME, 'emp_code': EMP_CODE,
                           'emp_design': DESIGNATION, 'present': total_present, 'absent': total_absent,
                           'leave': total_leave})
        else:
            for details in data:
                count += 1
                if details.ATTENDANCE_STATUS == "present":
                    total_present += 1
                elif details.ATTENDANCE_STATUS == "absent":
                    total_absent += 1
                elif details.ATTENDANCE_STATUS == "leave":
                    total_leave += 1

                class details_class:
                    id = count
                    IN_TIME = details.IN_TIME
                    OUT_TIME = details.OUT_TIME
                    LEAVE_CATEGORY = details.ATTENDANCE_STATUS
                    ATTENDANCE_DATE = details.ATTENDANCE_DATE
                    edit = EMP_CODE + "~" + details.ATTENDANCE_DATE

                em_mon_report.append(details_class)
            try:
                print("dghfdhsgbjhkrfkkfk")
                data = MONTHLY_ATTENDANCE_DETAILS.objects.get(EMP_CODE=request.POST.get('emp_code'),
                                                              MONTH_YEAR=request.POST.get(
                                                                  'date_month'))

                MONTHLY_ATTENDANCE_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_code'),
                                                          MONTH_YEAR=request.POST.get(
                                                              'date_month')).update(
                    TOTAL_PRESENT=total_present,
                    TOTAL_ABSENT=total_absent,
                    TOTAL_LEAVE=total_leave,
                )
            except MONTHLY_ATTENDANCE_DETAILS.DoesNotExist:
                print("dghfdhsgbjh")
                monthly_attendance = MONTHLY_ATTENDANCE_DETAILS(
                    EMP_CODE=request.POST.get('emp_code'),
                    EMP_NAME=EMP_NAME,
                    DESIGNATION=DESIGNATION,
                    TOTAL_PRESENT=total_present,
                    TOTAL_ABSENT=total_absent,
                    TOTAL_LEAVE=total_leave,
                    MONTH_YEAR=request.POST.get('date_month'),
                )
                monthly_attendance.save()
            return render(request, 'emp_daily_attendance.html',
                          {'data': em_mon_report, 'month_att': request.POST.get('date_month'),
                           'emp_name': EMP_NAME, 'emp_code': EMP_CODE,
                           'emp_design': DESIGNATION, 'present': total_present, 'absent': total_absent,
                           'leave': total_leave})
    else:
        emp_code = request.GET.get("secure")
        if emp_code is not None:
            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMPANY',
                                                                 'EMP_SAL').get(EMP_CODE=emp_code)
            emp_name = data.NEW_EMP.EMP_NAME
            emp_design = data.EMP_COMPANY.DESIGNATION
            return render(request, 'select_month_att.html',
                          {'emp_code': emp_code, 'emp_name': emp_name, 'emp_design': emp_design})

        else:
            return redirect(reverse('DailY_Attendance_Manegment'))


@login_required(login_url='login')
def daily_att_edit(request):
    if request.method == 'POST':
        att_month = request.POST.get('last_update_date').split('-')
        year = att_month[0]
        month = att_month[1]
        month_year = month + "-" + year
        print(month_year)
        data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                             'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
        EMP_NAME = data.NEW_EMP.EMP_NAME
        DESIGNATION = data.EMP_COMPANY.DESIGNATION
        EMP_DAILY_ATTENDANCE_LIST.objects.filter(EMP_CODE=request.POST.get('emp_code'),
                                                 ATTENDANCE_DATE=request.POST.get('last_update_date')).update(
            IN_TIME=request.POST.get('in_time'),
            OUT_TIME=request.POST.get('out_time'),
            ATTENDANCE_STATUS=request.POST.get('leave_category'),
        )
        EMP_DAILY_ATTENDANCE_UPDATED.objects.filter(EMP_CODE=request.POST.get('emp_code'),
                                                    LAST_UPDATE_DATE=request.POST.get('last_update_date')).update(
            IN_TIME=request.POST.get('in_time'),
            OUT_TIME=request.POST.get('out_time'),
            ATTENDANCE_STATUS=request.POST.get('leave_category'),
        )
        data = EMP_DAILY_ATTENDANCE_LIST.objects.filter(EMP_CODE=request.POST.get('emp_code'),
                                                        ATTENDANCE_MONTH=month_year)
        em_mon_report = []
        count = 0
        total_present = 0
        total_absent = 0
        total_leave = 0
        if not data:
            error_messege = "data_is_empty"
            return render(request, 'emp_daily_attendance.html',
                          {'data': error_messege, 'month_att': month_year,
                           'emp_name': EMP_NAME, 'emp_code': request.POST.get('emp_code'),
                           'emp_design': DESIGNATION, 'present': total_present, 'absent': total_absent,
                           'leave': total_leave})
        else:
            for details in data:
                count += 1
                if details.ATTENDANCE_STATUS == "present":
                    total_present += 1
                elif details.ATTENDANCE_STATUS == "absent":
                    total_absent += 1
                elif details.ATTENDANCE_STATUS == "leave":
                    total_leave += 1

                class details_class:
                    id = count
                    IN_TIME = details.IN_TIME
                    OUT_TIME = details.OUT_TIME
                    LEAVE_CATEGORY = details.ATTENDANCE_STATUS
                    ATTENDANCE_DATE = details.ATTENDANCE_DATE
                    edit = request.POST.get('emp_code') + "~" + details.ATTENDANCE_DATE

                em_mon_report.append(details_class)
            MONTHLY_ATTENDANCE_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_code'),
                                                      MONTH_YEAR=month_year).update(
                TOTAL_PRESENT=total_present,
                TOTAL_ABSENT=total_absent,
                TOTAL_LEAVE=total_leave,
            )
            return render(request, 'emp_daily_attendance.html',
                          {'data': em_mon_report, 'month_att': month_year,
                           'emp_name': EMP_NAME, 'emp_code': request.POST.get('emp_code'),
                           'emp_design': DESIGNATION, 'present': total_present, 'absent': total_absent,
                           'leave': total_leave})

    else:
        emp_code = request.GET.get("secure")
        if emp_code is not None:
            emp_code = request.GET.get("secure").split('~')
            print(emp_code[1], "ooooo")
            data = EMP_DAILY_ATTENDANCE_LIST.objects.filter(EMP_CODE=emp_code[0], ATTENDANCE_DATE=emp_code[1])
            return render(request, 'edit_daily_att.html', {'data': data})

        else:
            return redirect(reverse('DailY_Attendance_Manegment'))


@login_required(login_url='login')
def daily_att_update(request):
    if request.method == 'POST':
        total_present = 0
        total_absent = 0
        total_leave = 0
        if not request.POST.get('in_time') or not request.POST.get('out_time'):
            in_time = "00.00"
            out_time = "00.00"
        else:
            in_time = request.POST.get('in_time')
            out_time = request.POST.get('out_time')
        att_month = request.POST.get('last_update_date').split('-')
        year = att_month[0]
        month = att_month[1]
        data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                             'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
        EMP_NAME = data.NEW_EMP.EMP_NAME
        DESIGNATION = data.EMP_COMPANY.DESIGNATION
        EMP_DAILY_ATTENDANCE_UPDATED.objects.filter(EMP_CODE=request.POST.get('emp_code')).update(
            IN_TIME=in_time,
            OUT_TIME=out_time,
            ATTENDANCE_STATUS=request.POST.get('leave_category'),
            LAST_UPDATE_DATE=request.POST.get('last_update_date'),
        )
        try:
            emp_code_check = EMP_DAILY_ATTENDANCE_LIST.objects.get(EMP_CODE=request.POST.get('emp_code'),
                                                                   ATTENDANCE_DATE=request.POST.get(
                                                                       'last_update_date'))
            EMP_DAILY_ATTENDANCE_LIST.objects.filter(EMP_CODE=request.POST.get('emp_code'),
                                                     ATTENDANCE_DATE=request.POST.get('last_update_date')).update(
                IN_TIME=in_time,
                OUT_TIME=out_time,
                ATTENDANCE_STATUS=request.POST.get('leave_category'),
                ATTENDANCE_DATE=request.POST.get('last_update_date'),
                ATTENDANCE_MONTH=month + "-" + year,
            )
        except EMP_DAILY_ATTENDANCE_LIST.DoesNotExist:
            emp_daily_attendance = EMP_DAILY_ATTENDANCE_LIST(
                EMP_CODE=request.POST.get('emp_code'),
                EMP_NAME=EMP_NAME,
                DESIGNATION=DESIGNATION,
                IN_TIME=in_time,
                OUT_TIME=out_time,
                ATTENDANCE_STATUS=request.POST.get('leave_category'),
                ATTENDANCE_DATE=request.POST.get('last_update_date'),
                ATTENDANCE_MONTH=month + "-" + year,
            )
            emp_daily_attendance.save()
        try:
            att_check = EMP_DAILY_ATTENDANCE_UPDATED.objects.get(EMP_CODE=request.POST.get('emp_code'),
                                                                 LAST_UPDATE_DATE=request.POST.get('last_update_date'))
        except EMP_DAILY_ATTENDANCE_UPDATED.DoesNotExist:
            try:
                print("dghfdhsgbjhkrfkkfk")
                data = MONTHLY_ATTENDANCE_DETAILS.objects.get(EMP_CODE=request.POST.get('emp_code'),
                                                              MONTH_YEAR=month + "-" + year)

                total_present = int(data.TOTAL_PRESENT)
                total_absent = int(data.TOTAL_ABSENT)
                total_leave = int(data.TOTAL_LEAVE)

                if request.POST.get('leave_category') == "leave":
                    total_leave += 1
                elif request.POST.get('leave_category') == "present":
                    total_present += 1
                elif request.POST.get('leave_category') == "absent":
                    total_absent += 1
                MONTHLY_ATTENDANCE_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_code'),
                                                          MONTH_YEAR=month + "-" + year).update(
                    TOTAL_PRESENT=total_present,
                    TOTAL_ABSENT=total_absent,
                    TOTAL_LEAVE=total_leave,
                )
            except MONTHLY_ATTENDANCE_DETAILS.DoesNotExist:
                print("dghfdhsgbjh")
                if request.POST.get('leave_category') == "leave":
                    total_leave += 1
                elif request.POST.get('leave_category') == "present":
                    total_present += 1
                elif request.POST.get('leave_category') == "absent":
                    total_absent += 1
                monthly_attendance = MONTHLY_ATTENDANCE_DETAILS(
                    EMP_CODE=request.POST.get('emp_code'),
                    EMP_NAME=EMP_NAME,
                    DESIGNATION=DESIGNATION,
                    TOTAL_PRESENT=total_present,
                    TOTAL_ABSENT=total_absent,
                    TOTAL_LEAVE=total_leave,
                    MONTH_YEAR=month + "-" + year,
                )
                monthly_attendance.save()

        return redirect(reverse('DailY_Attendance_Manegment'))
    else:
        emp_code = request.GET.get("secure")
        print(emp_code)
        data = EMP_DAILY_ATTENDANCE_UPDATED.objects.filter(EMP_CODE=emp_code)
        return render(request, 'daily_att_update.html', {'data': data})


@login_required(login_url='login')
def leave_application_list(request):
    if 'New_Client_Req' not in request.session:
        data = LEAVE_APPLICATION_LIST.objects.all()
        return render(request, 'leave_application_list.html', {'data': data})
    else:
        session_client_name = request.session['New_Client_Req']
        del request.session["New_Client_Req"]
        request.session.modified = True
        data = LEAVE_APPLICATION_LIST.objects.all()
        return render(request, 'leave_application_list.html',
                      {'data': data, 'session_client_name': session_client_name})


@login_required(login_url='login')
def leave_category_list(request):
    if 'New_Client_Req' not in request.session:
        data = LEAVE_CATEGORY_LIST.objects.all()
        data_list = []
        count = 0
        for details in data:
            count += 1

            class details_class:
                ID = count
                CATEGORY_NAME = details.CATEGORY_NAME
                CATEGORY_DESCRIPTION = details.CATEGORY_DESCRIPTION
                STATUS = details.STATUS
                ADDED_DATE = details.ADDED_DATE

            data_list.append(details_class)
        return render(request, 'leave_category_list.html', {'data': data_list})
    else:
        session_client_name = request.session['New_Client_Req']

        del request.session["New_Client_Req"]
        request.session.modified = True
        data = LEAVE_CATEGORY_LIST.objects.all()
        data_list = []
        count = 0
        print(data)
        for details in data:
            count += 1

            class details_class:
                ID = count
                CATEGORY_NAME = details.CATEGORY_NAME
                CATEGORY_DESCRIPTION = details.CATEGORY_DESCRIPTION
                STATUS = details.STATUS
                ADDED_DATE = details.ADDED_DATE

            data_list.append(details_class)
        return render(request, 'leave_category_list.html',
                      {'data': data_list, 'session_client_name': session_client_name})


@login_required(login_url='login')
def notice_list(request):
    if 'New_Client_Req' not in request.session:
        data = NOTICE_BOARD.objects.all()
        data_list = []
        count = 0
        for details in data:
            count += 1

            class details_class:
                ID = count
                TITLE = details.TITLE
                DESCRIPTION = details.DESCRIPTION
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        return render(request, 'notice_list.html', {'data': data_list})
    else:
        session_client_name = request.session['New_Client_Req']

        del request.session["New_Client_Req"]
        request.session.modified = True
        data = NOTICE_BOARD.objects.all()
        data_list = []
        count = 0
        print(data)
        for details in data:
            count += 1

            class details_class:
                ID = count
                TITLE = details.TITLE
                DESCRIPTION = details.DESCRIPTION
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS

            data_list.append(details_class)
        return render(request, 'notice_list.html', {'data': data_list, 'session_client_name': session_client_name})


@login_required(login_url='login')
def holidays_list(request):
    if 'New_Client_Req' not in request.session:
        data = HOLIDAYS.objects.all()
        data_list = []
        count = 0
        for details in data:
            count += 1

            class details_class:
                ID = count
                HOLIDAY_NAME = details.HOLIDAY_NAME
                DESCRIPTION = details.DESCRIPTION
                HOLIDAY_DATE = details.HOLIDAY_DATE
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        return render(request, 'holidays_list.html', {'data': data_list})
    else:
        session_client_name = request.session['New_Client_Req']

        del request.session["New_Client_Req"]
        request.session.modified = True
        data = HOLIDAYS.objects.all()
        data_list = []
        count = 0
        print(data)
        for details in data:
            count += 1

            class details_class:
                ID = count
                HOLIDAY_NAME = details.HOLIDAY_NAME
                DESCRIPTION = details.DESCRIPTION
                HOLIDAY_DATE = details.HOLIDAY_DATE
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        return render(request, 'holidays_list.html', {'data': data_list, 'session_client_name': session_client_name})


@login_required(login_url='login')
def client_type_list(request):
    if 'New_Client_Req' not in request.session:
        data = CLIENT_TYPE.objects.all()
        data_list = []
        count = 0
        db_value = "not_null"
        for details in data:
            count += 1

            class details_class:
                ID = count
                CLIENT_TYPE = details.CLIENT_TYPE
                DESCRIPTION = details.DESCRIPTION
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        if not data_list:
            db_value = "null"
        return render(request, 'client_type_list.html', {'data': data_list, 'db_value': db_value})
    else:
        session_client_name = request.session['New_Client_Req']
        del request.session["New_Client_Req"]
        request.session.modified = True
        data = CLIENT_TYPE.objects.all()
        data_list = []
        count = 0
        db_value = "not_null"
        for details in data:
            count += 1

            class details_class:
                ID = count
                CLIENT_TYPE = details.CLIENT_TYPE
                DESCRIPTION = details.DESCRIPTION
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        if not data_list:
            db_value = "null"
        return render(request, 'client_type_list.html',
                      {'data': data_list, 'session_client_name': session_client_name, 'db_value': db_value})


@login_required(login_url='login')
def designation_list(request):
    if 'New_Client_Req' not in request.session:
        data = DESIGNATION_LIST.objects.all()
        data_list = []
        count = 0
        db_value = "not_null"
        for details in data:
            count += 1

            class details_class:
                ID = count
                DESIGNATION = details.DESIGNATION
                DESCRIPTION = details.DESCRIPTION
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        if not data_list:
            db_value = "null"
        return render(request, 'designation_list.html', {'data': data_list, 'db_value': db_value})
    else:
        session_client_name = request.session['New_Client_Req']
        del request.session["New_Client_Req"]
        request.session.modified = True
        data = DESIGNATION_LIST.objects.all()
        data_list = []
        count = 0
        db_value = "not_null"
        for details in data:
            count += 1

            class details_class:
                ID = count
                DESIGNATION = details.DESIGNATION
                DESCRIPTION = details.DESCRIPTION
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        if not data_list:
            db_value = "null"
        return render(request, 'designation_list.html',
                      {'data': data_list, 'session_client_name': session_client_name, 'db_value': db_value})


@login_required(login_url='login')
def event_list(request):
    if 'New_Client_Req' not in request.session:
        data = PERSONAL_EVENT.objects.all()
        data_list = []
        count = 0
        db_value = "not_null"
        for details in data:
            count += 1

            class details_class:
                ID = count
                EVENT_NAME = details.EVENT_NAME
                START_DATE = details.START_DATE
                END_DATE = details.END_DATE
                DESCRIPTION = details.DESCRIPTION
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        if not data_list:
            db_value = "null"
        return render(request, 'event_list.html', {'data': data_list, 'db_value': db_value})
    else:
        session_client_name = request.session['New_Client_Req']
        del request.session["New_Client_Req"]
        request.session.modified = True
        data = PERSONAL_EVENT.objects.all()
        data_list = []
        count = 0
        db_value = "not_null"
        for details in data:
            count += 1

            class details_class:
                ID = count
                EVENT_NAME = details.EVENT_NAME
                START_DATE = details.START_DATE
                END_DATE = details.END_DATE
                DESCRIPTION = details.DESCRIPTION
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        if not data_list:
            db_value = "null"
        return render(request, 'event_list.html',
                      {'data': data_list, 'session_client_name': session_client_name, 'db_value': db_value})


@login_required(login_url='login')
def country_list(request):
    if request.method == 'POST':
        print(request.POST.get("submit"))
        if request.POST.get("submit") == "add_country":
            add_country = COUNTRY_LIST(
                COUNTRY_NAME=request.POST.get('country_name'),
            )
            add_country.save()
            request.session['New_Client_Req'] = "Successfully Add Country " + request.POST.get(
                'country_name')
        if request.POST.get("submit") == "add_state":
            try:
                last_id = STATE_LIST.objects.latest('ID')
                increse = int(last_id.STATE_ID) + 1
                new_id = "0" + str(increse)
            except STATE_LIST.DoesNotExist:
                new_id = "01"
            add_state = STATE_LIST(
                STATE_ID=new_id,
                COUNTRY_NAME=request.POST.get('country_name'),
                STATE_NAME=request.POST.get('state_name'),
            )
            add_state.save()
            request.session['New_Client_Req'] = "Successfully Add State " + request.POST.get(
                'state_name')
        if request.POST.get("submit") == "add_city":
            try:
                last_id = CITY_LIST.objects.latest('ID')
                increse = int(last_id.CITY_ID) + 1
                new_id = "00" + str(increse)
            except CITY_LIST.DoesNotExist:
                new_id = "001"
            add_country = CITY_LIST(
                CITY_ID=new_id,
                COUNTRY_NAME=request.POST.get('country_name'),
                STATE_NAME=request.POST.get('state_name'),
                CITY_NAME=request.POST.get('city_name'),
            )
            add_country.save()
            request.session['New_Client_Req'] = "Successfully Add City " + request.POST.get(
                'city_name')
        return redirect(reverse('Country_List'))
    else:
        country_list = COUNTRY_LIST.objects.all()
        state_list = STATE_LIST.objects.all()
        city_list = CITY_LIST.objects.all()

        country_data_list = []
        state_data_list = []
        city_data_list = []

        country = "not_null"
        state = "not_null"
        city = "not_null"
        count = 0
        for country in country_list:
            count += 1

            class country_class:
                ID = count
                COUNTRY_NAME = country.COUNTRY_NAME
                Db_id = country.ID

            country_data_list.append(country_class)
        count = 0
        for state in state_list:
            count += 1

            class state_class:
                ID = count
                STATE_NAME = state.STATE_NAME
                COUNTRY_NAME = state.COUNTRY_NAME
                State_id = state.STATE_ID

            state_data_list.append(state_class)
        count = 0
        for city in city_list:
            count += 1

            class city_class:
                ID = count
                CITY_NAME = city.CITY_NAME
                STATE_NAME = city.STATE_NAME
                COUNTRY_NAME = city.COUNTRY_NAME
                CITY_ID = city.CITY_ID

            city_data_list.append(city_class)
        if not country_data_list:
            country = "null"
        if not state_data_list:
            state = "null"
        if not city_data_list:
            city = "null"
        if 'New_Client_Req' not in request.session:
            value = {
                'country': country,
                'country_data_list': country_data_list,
                'state': state,
                'state_data_list': state_data_list,
                'city': city,
                'city_data_list': city_data_list,
            }
            return render(request, 'country_list.html', value)
        else:
            session_client_name = request.session['New_Client_Req']
            del request.session["New_Client_Req"]
            request.session.modified = True
            value = {
                'country': country,
                'country_data_list': country_data_list,
                'state': state,
                'state_data_list': state_data_list,
                'city': city,
                'city_data_list': city_data_list,
                'session_client_name': session_client_name,
            }
            return render(request, 'country_list.html', value)


@login_required(login_url='login')
def client_list(request):
    if request.method == 'POST':
        if request.POST.get("submit") == "add_client":
            add_country = CLIENT_LIST(
                CLIENT=request.POST.get('client_name'),
            )
            add_country.save()
            request.session['New_Client_Req'] = "Successfully Add Client " + request.POST.get(
                'client_name')
        if request.POST.get("submit") == "add_unit":
            try:
                last_id = UNIT_LIST.objects.latest('ID')
                increse = int(last_id.UNIT_ID) + 1
                new_id = "0" + str(increse)
            except UNIT_LIST.DoesNotExist:
                new_id = "01"
            add_state = UNIT_LIST(
                UNIT_ID=new_id,
                CLIENT=request.POST.get('client_name'),
                UNIT=request.POST.get('unit_name'),
            )
            add_state.save()
            request.session['New_Client_Req'] = "Successfully Add Unit " + request.POST.get(
                'unit_name')
        return redirect(reverse('Client_List'))
    else:
        client_list = CLIENT_LIST.objects.all()
        unit_list = UNIT_LIST.objects.all()

        client_data_list = []
        unit_data_list = []

        client = "not_null"
        unit = "not_null"
        count = 0
        for client in client_list:
            count += 1

            class client_class:
                ID = count
                CLIENT = client.CLIENT
                Db_id = client.ID

            client_data_list.append(client_class)
        count = 0
        for unit in unit_list:
            count += 1

            class unit_class:
                ID = count
                UNIT = unit.UNIT
                CLIENT = unit.CLIENT
                Unit_id = unit.UNIT_ID

            unit_data_list.append(unit_class)
        count = 0
        if not client_data_list:
            client = "null"
        if not unit_data_list:
            unit = "null"
        if 'New_Client_Req' not in request.session:
            value = {
                'client': client,
                'client_data_list': client_data_list,
                'unit': unit,
                'unit_data_list': unit_data_list,
            }
            return render(request, 'client_list.html', value)
        else:
            session_client_name = request.session['New_Client_Req']
            del request.session["New_Client_Req"]
            request.session.modified = True
            value = {
                'client': client,
                'client_data_list': client_data_list,
                'unit': unit,
                'unit_data_list': unit_data_list,
                'session_client_name': session_client_name,
            }
            return render(request, 'client_list.html', value)


@login_required(login_url='login')
def client_details(request):
    if request.method == 'POST':
        try:
            last_id = CLIENT_DETAILS.objects.latest('ID')
            increse = int(last_id.CLIENT_ID) + 1
            new_id = "0" + str(increse)
        except CLIENT_DETAILS.DoesNotExist:
            new_id = "01"
        add_client = CLIENT_DETAILS(
            CLIENT_ID=new_id,
            CLIENT=request.POST.get('client_name'),
            COUNTRY_NAME=request.POST.get('country_name'),
            STATE_NAME=request.POST.get('state_name'),
            DISTRICT_NAME=request.POST.get('district_name'),
            BRANCH_NAME=request.POST.get('branch_name'),
            AREA_NAME=request.POST.get('area_name'),
            UNIT=request.POST.get('unit'),
            E_MAIL=request.POST.get('client_email'),
            WEB=request.POST.get('client_ph'),
            CONTACT_NO=request.POST.get('client_web'),
            ADDRESS=request.POST.get('address'),
        )
        add_client.save()
        request.session['New_Client_Req'] = "Successfully Add Client " + request.POST.get(
            'client_name')
        return redirect(reverse('Client_Details'))

    else:
        client_list = CLIENT_DETAILS.objects.all()

        client = "not_null"

        if not client_list:
            client = "null"

        if 'New_Client_Req' not in request.session:
            value = {
                'client': client,
                'client_data_list': client_list,
            }
            return render(request, 'client_list.html', value)
        else:
            session_client_name = request.session['New_Client_Req']
            del request.session["New_Client_Req"]
            request.session.modified = True
            value = {
                'client': client,
                'client_data_list': client_list,
                'session_client_name': session_client_name,
            }
            return render(request, 'client_list.html', value)


@login_required(login_url='login')
def award_category_list(request):
    if 'New_Client_Req' not in request.session:
        data = AWARD_CATEGORY_LIST.objects.all()
        data_list = []
        count = 0
        db_value = "not_null"
        for details in data:
            count += 1

            class details_class:
                ID = count
                AWARD_CATEGORY = details.AWARD_CATEGORY
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        if not data_list:
            db_value = "null"
        return render(request, 'award_category_list.html', {'data': data_list, 'db_value': db_value})
    else:
        db_value = "not_null"
        session_client_name = request.session['New_Client_Req']
        del request.session["New_Client_Req"]
        request.session.modified = True
        data = AWARD_CATEGORY_LIST.objects.all()
        data_list = []
        count = 0
        print(data)
        for details in data:
            count += 1

            class details_class:
                ID = count
                AWARD_CATEGORY = details.AWARD_CATEGORY
                CREATED_AT = details.CREATED_AT
                STATUS = details.STATUS
                Db_id = details.ID

            data_list.append(details_class)
        if not data_list:
            db_value = "null"
        return render(request, 'award_category_list.html',
                      {'data': data_list, 'session_client_name': session_client_name, 'db_value': db_value})


@login_required(login_url='login')
def expense_category_list(request):
    if 'New_Client_Req' not in request.session:
        data = EXPENSE_CATEGORY_LIST.objects.all()
        data_list = []
        count = 0
        for details in data:
            count += 1

            class details_class:
                ID = count
                EXP_PURPOSE = details.EXP_PURPOSE
                CREATED_BY = details.CREATED_BY

            data_list.append(details_class)
        return render(request, 'expense_category_list.html', {'data': data_list})
    else:
        session_client_name = request.session['New_Client_Req']

        del request.session["New_Client_Req"]
        request.session.modified = True
        data = EXPENSE_CATEGORY_LIST.objects.all()
        data_list = []
        count = 0
        print(data)
        for details in data:
            count += 1

            class details_class:
                ID = count
                EXP_PURPOSE = details.EXP_PURPOSE
                CREATED_BY = details.CREATED_BY

            data_list.append(details_class)
        return render(request, 'expense_category_list.html',
                      {'data': data_list, 'session_client_name': session_client_name})


@login_required(login_url='login')
def expense_list(request):
    if 'New_Client_Req' not in request.session:
        last_id = new_emp_reg.objects.count()
        print(last_id)
        data = EMP_EXPENSE_DETAILS.objects.all()
        return render(request, 'expense_list.html', {'data': data})
    else:

        session_client_name = request.session['New_Client_Req']

        del request.session["New_Client_Req"]
        request.session.modified = True
        emp_count = new_emp_reg.objects.count()
        print(emp_count)
        data = EMP_EXPENSE_DETAILS.objects.all()
        return render(request, 'expense_list.html', {'data': data, 'session_client_name': session_client_name})


def certificate_list(request):
    if 'New_Client_Req' not in request.session:
        data = EMP_CERTIFICATE_DETAILS.objects.all()
        return render(request, 'certificate_list.html', {'data': data})
    else:
        session_client_name = request.session['New_Client_Req']
        del request.session["New_Client_Req"]
        request.session.modified = True
        data = EMP_CERTIFICATE_DETAILS.objects.all()
        return render(request, 'certificate_list.html', {'data': data, 'session_client_name': session_client_name})


def award_list(request):
    if 'New_Client_Req' not in request.session:
        data = EMP_AWARD_LIST.objects.all()
        return render(request, 'award_list.html', {'data': data})
    else:
        session_client_name = request.session['New_Client_Req']
        session_client_code = request.session['New_Client_Code']
        del request.session["New_Client_Req"]
        del request.session["New_Client_Code"]
        request.session.modified = True
        data = EMP_AWARD_LIST.objects.all()
        return render(request, 'award_list.html', {'data': data, 'session_client_name': session_client_name,
                                                   'session_client_code': session_client_code})


@login_required(login_url='login')
def new_increment_list(request):
    if 'New_Client_Req' not in request.session:
        data = EMP_INCREMENT_DETAILS.objects.all()
        return render(request, 'increment_list.html', {'data': data})
    else:

        session_client_name = request.session['New_Client_Req']
        session_client_code = request.session['New_Client_Code']

        del request.session["New_Client_Req"]
        del request.session["New_Client_Code"]
        request.session.modified = True
        data = EMP_INCREMENT_DETAILS.objects.all()
        return render(request, 'increment_list.html', {'data': data, 'session_client_name': session_client_name,
                                                       'session_client_code': session_client_code})


@login_required(login_url='login')
def new_bonus_list(request):
    if 'New_Client_Req' not in request.session:
        data = EMP_BONUS_DETAILS.objects.all()
        return render(request, 'bonus_list.html', {'data': data})
    else:

        session_client_name = request.session['New_Client_Req']
        session_client_code = request.session['New_Client_Code']

        del request.session["New_Client_Req"]
        del request.session["New_Client_Code"]
        request.session.modified = True
        data = EMP_BONUS_DETAILS.objects.all()
        return render(request, 'bonus_list.html', {'data': data, 'session_client_name': session_client_name,
                                                   'session_client_code': session_client_code})


@login_required(login_url='login')
def manuel_setting(request):
    return render(request, 'manuel_setting.html')


@login_required(login_url='login')
def daily_attendance_manegement(request):
    if 'New_Client_Req' not in request.session:
        data = EMP_DAILY_ATTENDANCE_UPDATED.objects.all()
        return render(request, 'manage_daily_attendance.html', {'data': data})
    else:

        session_client_name = request.session['New_Client_Req']
        session_client_code = request.session['New_Client_Code']

        del request.session["New_Client_Req"]
        del request.session["New_Client_Code"]
        request.session.modified = True
        data = EMP_DAILY_ATTENDANCE_UPDATED.objects.all()
        return render(request, 'manage_daily_attendance.html',
                      {'data': data, 'session_client_name': session_client_name,
                       'session_client_code': session_client_code})


@login_required(login_url='login')
def daily_attendance_list(request):
    if 'New_Client_Req' not in request.session:
        data = EMP_DAILY_ATTENDANCE_LIST.objects.all()
        return render(request, 'emp_daily_attendance.html', {'data': data})
    else:

        session_client_name = request.session['New_Client_Req']
        session_client_code = request.session['New_Client_Code']

        del request.session["New_Client_Req"]
        del request.session["New_Client_Code"]
        request.session.modified = True
        data = EMP_DAILY_ATTENDANCE_LIST.objects.all()
        return render(request, 'emp_daily_attendance.html', {'data': data, 'session_client_name': session_client_name,
                                                             'session_client_code': session_client_code})


@login_required(login_url='login')
def loan_list(request):
    if 'New_Client_Req' not in request.session:
        data = EMP_LOAN_DETAILS.objects.all()
        return render(request, 'loan_list.html', {'data': data})
    else:

        session_client_name = request.session['New_Client_Req']
        session_client_code = request.session['New_Client_Code']

        del request.session["New_Client_Req"]
        del request.session["New_Client_Code"]
        request.session.modified = True
        data = EMP_LOAN_DETAILS.objects.all()
        return render(request, 'loan_list.html', {'data': data, 'session_client_name': session_client_name,
                                                  'session_client_code': session_client_code})


@login_required(login_url='login')
def advance_list(request):
    if 'New_Client_Req' not in request.session:
        data = EMP_ADVANCE_DETAILS.objects.all()
        return render(request, 'advance_list.html', {'data': data})
    else:

        session_client_name = request.session['New_Client_Req']
        session_client_code = request.session['New_Client_Code']

        del request.session["New_Client_Req"]
        del request.session["New_Client_Code"]
        request.session.modified = True
        data = EMP_ADVANCE_DETAILS.objects.all()
        return render(request, 'advance_list.html', {'data': data, 'session_client_name': session_client_name,
                                                     'session_client_code': session_client_code})


@login_required(login_url='login')
def edit_advance(request):
    if request.method == "POST":
        try:
            emp_code = EMP_ADVANCE_DETAILS.objects.filter(LAST_ADVANCE_UPDATED=request.POST.get('date_month'))
            error_messege = request.POST.get('date_month') + " is Already Updated"
            error_count = "1"
            print("try")
            return render(request, 'advance_list.html',
                          {'data': emp_code, 'err_msg': error_messege, 'err_count': error_count})

        except EMP_ADVANCE_DETAILS.DoesNotExist:
            given_amount = int(request.POST.get('given_amount')) + int(request.POST.get('giving_amount'))
            remaining_amount = int(request.POST.get('advance_amount')) - given_amount
            EMP_ADVANCE_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_code')).update(
                GIVING_AMOUNT=request.POST.get('giving_amount'),
                GIVEN_AMOUNT=given_amount,
                REMAINING_AMOUNT=remaining_amount,
                LAST_ADVANCE_UPDATED=request.POST.get('date_month'),
            )
            return redirect(reverse('Advance_List'))
    else:
        emp_code = request.GET.get('secure')
        if emp_code is not None:
            print(emp_code)
            emp_code = EMP_ADVANCE_DETAILS.objects.filter(EMP_CODE=emp_code)
            print(request.GET.get('secure'))
            return render(request, 'edit_advance.html', {'data': emp_code})
        else:
            print(emp_code)
            return redirect(reverse('Advance_List'))


@login_required(login_url='login')
def add_loan(request):
    if request.method == 'POST':
        try:
            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                 'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
            print(data)
            EMP_NAME = data.NEW_EMP.EMP_NAME
            DESIGNATION = data.EMP_COMPANY.DESIGNATION
            DATE = datetime.now().strftime("%Y-%m-%d")

            new_loan_register = EMP_LOAN_DETAILS(
                EMP_CODE=request.POST.get('emp_code'),
                EMP_NAME=EMP_NAME,
                DESIGNATION=DESIGNATION,
                LOAN_NAME=request.POST.get('loan_name'),
                LOAN_AMOUNT=request.POST.get('loan_amount'),
                NUMBER_OF_INSTALLMENT=request.POST.get('no_of_inst'),
                AMOUNT_OF_INSTALLMENT=request.POST.get('amount_of_inst'),
                REMAINING_OF_INSTALLMENT=0,
                LOAN_DESCRIPTION=request.POST.get('loan_description'),
                LOAN_ADDED_DATE=DATE,
            )
            new_loan_register.save()

            request.session['New_Client_Req'] = "Successfully Add Loan $ " + request.POST.get(
                'loan_amount')
            request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')

            return redirect(reverse('Loan_List'))  # We redirect to the same view

        except EMP_POLICE_VERFICATION.DoesNotExist:
            request.session['New_Client_Req'] = request.POST.get('emp_code') + " is Not Register"
            request.session['New_Client_Code'] = " "

            return render(request, 'add_loan.html')

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            print("new")
            return render(request, 'add_loan.html')
        else:
            print("old")
            session_client_name = request.session['New_Client_Req']
            session_client_code = request.session['New_Client_Code']

            del request.session["New_Client_Req"]
            del request.session["New_Client_Code"]
            request.session.modified = True

            return render(request, 'add_loan.html',
                          {'session_client_name': session_client_name, 'session_client_code': session_client_code})


@login_required(login_url='login')
def add_advance(request):
    if request.method == 'POST':
        try:
            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                 'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
            print(data)
            EMP_NAME = data.NEW_EMP.EMP_NAME
            DESIGNATION = data.EMP_COMPANY.DESIGNATION
            DATE = datetime.now().strftime("%Y-%m-%d")

            new_advance_register = EMP_ADVANCE_DETAILS(
                EMP_CODE=request.POST.get('emp_code'),
                EMP_NAME=EMP_NAME,
                DESIGNATION=DESIGNATION,
                ADVANCE_AMOUNT=request.POST.get('advance_amount'),
                REMAINING_AMOUNT=0,
                GIVEN_AMOUNT=0,
                GIVING_AMOUNT=0,
                LAST_ADVANCE_UPDATED="NO UPDATED",
                LOAN_ADDED_DATE=DATE,
            )
            new_advance_register.save()

            request.session['New_Client_Req'] = "Successfully Add Loan $ " + request.POST.get(
                'advance_amount')
            request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')

            return redirect(reverse('Advance_List'))  # We redirect to the same view

        except EMP_POLICE_VERFICATION.DoesNotExist:
            request.session['New_Client_Req'] = request.POST.get('emp_code') + " is Not Register"
            request.session['New_Client_Code'] = " "

            return render(request, 'add_advance.html')

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            print("new")
            return render(request, 'add_advance.html')
        else:
            print("old")
            session_client_name = request.session['New_Client_Req']
            session_client_code = request.session['New_Client_Code']

            del request.session["New_Client_Req"]
            del request.session["New_Client_Code"]
            request.session.modified = True

            return render(request, 'add_advance.html',
                          {'session_client_name': session_client_name, 'session_client_code': session_client_code})


@login_required(login_url='login')
def new_increment(request):
    if request.method == 'POST':
        try:
            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                 'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
            print(data)
            EMP_NAME = data.NEW_EMP.EMP_NAME
            DESIGNATION = data.EMP_COMPANY.DESIGNATION
            OLD_SALARY = data.EMP_SAL.FIXED_SALARY

            curent_salary = int(OLD_SALARY) + int(request.POST.get('increment_amount'))

            new_increment_register = EMP_INCREMENT_DETAILS(
                EMP_CODE=request.POST.get('emp_code'),
                EMP_NAME=EMP_NAME,
                DESIGNATION=DESIGNATION,
                OLD_SALARY=OLD_SALARY,
                INCREMENT_AMOUNT=request.POST.get('increment_amount'),
                CURRENT_SALARY=curent_salary,
                INCREMENT_PURPOSE=request.POST.get('incre_purpose'),
                INCREMENT_UPDATE_DATE=request.POST.get('date_month'),
            )
            new_increment_register.save()

            request.session['New_Client_Req'] = "Successfully Add Increment $ " + request.POST.get(
                'increment_amount')
            request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')

            return redirect(reverse('New_Increment'))  # We redirect to the same view

        except EMP_POLICE_VERFICATION.DoesNotExist:
            request.session['New_Client_Req'] = request.POST.get('emp_code') + " is Not Register"
            request.session['New_Client_Code'] = " "

            return render(request, 'add_increment.html')

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            print("new")
            return render(request, 'add_increment.html')
        else:
            print("old")
            session_client_name = request.session['New_Client_Req']
            session_client_code = request.session['New_Client_Code']

            del request.session["New_Client_Req"]
            del request.session["New_Client_Code"]
            request.session.modified = True

            return render(request, 'add_increment.html',
                          {'session_client_name': session_client_name, 'session_client_code': session_client_code})


@login_required(login_url='login')
def new_excepense_category(request):
    if request.method == 'POST':
        try:
            data = EXPENSE_CATEGORY_LIST.objects.get(EXP_PURPOSE=request.POST.get('purpose_name'))

            request.session['New_Client_Req'] = request.POST.get('purpose_name') + " is Already Exist"

            return render(request, 'create_expense_category.html')

        except EXPENSE_CATEGORY_LIST.DoesNotExist:
            new_expense_category = EXPENSE_CATEGORY_LIST(

                EXP_PURPOSE=request.POST.get('purpose_name'),
                CREATED_BY="Manager",
            )
            new_expense_category.save()
            request.session['New_Client_Req'] = "Successfully Add New Leave Category is" + request.POST.get(
                'purpose_name')

            return redirect(reverse('Expense_Category_List'))

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            print("new")
            return render(request, 'create_expense_category.html')
        else:
            print("old")
            session_client_name = request.session['New_Client_Req']

            del request.session["New_Client_Req"]
            request.session.modified = True

            return render(request, 'create_expense_category.html',
                          {'session_client_name': session_client_name})


@login_required(login_url='login')
def new_excepense(request):
    if request.method == 'POST':
        try:
            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                 'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
            print(data)
            EMP_NAME = data.NEW_EMP.EMP_NAME
            DESIGNATION = data.EMP_COMPANY.DESIGNATION

            new_expense_register = EMP_EXPENSE_DETAILS(
                EMP_CODE=request.POST.get('emp_code'),
                EMP_NAME=EMP_NAME,
                DESIGNATION=DESIGNATION,
                EXPENSE_DATE=request.POST.get('expense_date'),
                EXPENSE_AMOUNT=request.POST.get('expense_amount'),
                EXPENSE_PURPOSE=request.POST.get('expense_purpose'),
                REMARK=request.POST.get('remark'),
            )
            new_expense_register.save()

            request.session['New_Client_Req'] = "Successfully Add Expense Amount $ " + request.POST.get(
                'expense_amount')
            request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')

            return redirect(reverse('Expense_List'))  # We redirect to the same view

        except EMP_POLICE_VERFICATION.DoesNotExist:
            request.session['New_Client_Req'] = request.POST.get('emp_code') + " is Not Register"
            request.session['New_Client_Code'] = " "

            return render(request, 'create_expense.html')

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            print("new")
            data = EXPENSE_CATEGORY_LIST.objects.all()
            return render(request, 'create_expense.html', {'data': data})
        else:
            print("old")
            session_client_name = request.session['New_Client_Req']
            session_client_code = request.session['New_Client_Code']

            del request.session["New_Client_Req"]
            del request.session["New_Client_Code"]
            request.session.modified = True

            return render(request, 'create_expense.html',
                          {'session_client_name': session_client_name, 'session_client_code': session_client_code})


@login_required(login_url='login')
def new_leave_gategory(request):
    if request.method == 'POST':
        try:
            data = LEAVE_CATEGORY_LIST.objects.get(CATEGORY_NAME=request.POST.get('leave_name'))
            print(request.POST.get('category_description'), "space")

            request.session['New_Client_Req'] = request.POST.get('leave_name') + " is Already Exist"

            return render(request, 'new_leave_category.html')

        except LEAVE_CATEGORY_LIST.DoesNotExist:
            DATE = datetime.now().strftime("%d-%B-%Y")
            new_expense_category = LEAVE_CATEGORY_LIST(
                CATEGORY_NAME=request.POST.get('leave_name'),
                CATEGORY_DESCRIPTION=request.POST.get('category_description'),
                STATUS=request.POST.get('status'),
                ADDED_DATE=DATE,
            )
            new_expense_category.save()
            request.session['New_Client_Req'] = "Successfully Add New Expense Category is" + request.POST.get(
                'leave_name')

            return redirect(reverse('Leave_Category_List'))

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            print("new")
            return render(request, 'new_leave_category.html')
        else:
            print("old")
            session_client_name = request.session['New_Client_Req']

            del request.session["New_Client_Req"]
            request.session.modified = True

            return render(request, 'new_leave_category.html',
                          {'session_client_name': session_client_name})


@login_required(login_url='login')
def add_certificate(request):
    if request.method == 'POST':
        try:

            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                 'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
            try:
                data1 = EMP_CERTIFICATE_DETAILS.objects.get(EMP_CODE=request.POST.get('emp_code'),
                                                            CERTIFICATE_TYPE=request.POST.get('certificate_type'))

                request.session['New_Client_Req'] = request.POST.get(
                    'certificate_type') + " Certificate is Already Exist for this employee"

                return render(request, 'add_certificate.html')
            except EMP_CERTIFICATE_DETAILS.DoesNotExist:
                EMP_NAME = data.NEW_EMP.EMP_NAME
                DESIGNATION = data.EMP_COMPANY.DESIGNATION
                DATE = datetime.now().strftime("%d-%B-%Y")
                add_certificate = EMP_CERTIFICATE_DETAILS(
                    EMP_CODE=request.POST.get('emp_code'),
                    EMP_NAME=EMP_NAME,
                    DESIGNATION=DESIGNATION,
                    CERTIFICATE_TYPE=request.POST.get('certificate_type'),
                    CERTIFICATE_DESCRIPTION=request.POST.get('certificate_description'),
                    ADD_DATE=DATE,
                )
                add_certificate.save()
                request.session['New_Client_Req'] = request.POST.get(
                    'certificate_type') + " Certificate is Successfully Created"

                return redirect(reverse('Certificate_List'))
        except EMP_POLICE_VERFICATION.DoesNotExist:
            request.session['New_Client_Req'] = request.POST.get('emp_code') + " is Not Register"
            return render(request, 'add_certificate.html')

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            print("new")
            return render(request, 'add_certificate.html')
        else:
            print("old")
            session_client_name = request.session['New_Client_Req']

            del request.session["New_Client_Req"]
            request.session.modified = True

            return render(request, 'add_certificate.html',
                          {'session_client_name': session_client_name})


@login_required(login_url='login')
def new_leave_application(request):
    if request.method == 'POST':
        try:
            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                 'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
            DATE = datetime.now().strftime("%d-%B-%Y")
            print(data)
            EMP_NAME = data.NEW_EMP.EMP_NAME
            DESIGNATION = data.EMP_COMPANY.DESIGNATION
            start_leave = request.POST.get('start_date').split('-')
            end_leave = request.POST.get('end_date').split('-')
            leave_days = (int(end_leave[2]) + 1) - int(start_leave[2])
            new_leve_application = LEAVE_APPLICATION_LIST(
                EMP_CODE=request.POST.get('emp_code'),
                EMP_NAME=EMP_NAME,
                DESIGNATION=DESIGNATION,
                REASON=request.POST.get('leave_reason'),
                START_DATE=request.POST.get('start_date'),
                END_DATE=request.POST.get('end_date'),
                LEAVE_CATEGORY=request.POST.get('leave_category'),
                LEAVE_DAYS=leave_days,
                STATUS="Pending",
                ADDED_DATE=DATE,
            )
            new_leve_application.save()

            request.session[
                'New_Client_Req'] = "Successfully Add Leave Application Under Category is " + request.POST.get(
                'leave_category')
            request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')

            return redirect(reverse('Leave_Application_List'))

        except EMP_POLICE_VERFICATION.DoesNotExist:
            request.session['New_Client_Req'] = request.POST.get('emp_code') + " is Not Register"
            request.session['New_Client_Code'] = " "

            return render(request, 'new_leave_application.html')

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            print("new")
            data = LEAVE_CATEGORY_LIST.objects.all()
            return render(request, 'new_leave_application.html', {'data': data})
        else:
            data = LEAVE_CATEGORY_LIST.objects.all()
            print("old")
            session_client_name = request.session['New_Client_Req']

            del request.session["New_Client_Req"]
            request.session.modified = True

            return render(request, 'new_leave_application.html',
                          {'session_client_name': session_client_name})


@login_required(login_url='login')
def new_bonus(request):
    if request.method == 'POST':
        try:
            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                 'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
            print(data)
            EMP_NAME = data.NEW_EMP.EMP_NAME
            DESIGNATION = data.EMP_COMPANY.DESIGNATION

            new_bonus_register = EMP_BONUS_DETAILS(
                EMP_CODE=request.POST.get('emp_code'),
                EMP_NAME=EMP_NAME,
                DESIGNATION=DESIGNATION,
                BONUS_NAME=request.POST.get('bonus_name'),
                BONUS_AMOUNT=request.POST.get('bonus_amount'),
                BONUS_DESCRIPTION=request.POST.get('bonus_description'),
                BONUS_UPDATE_DATE=request.POST.get('date_month'),
            )
            new_bonus_register.save()

            request.session['New_Client_Req'] = "Successfully Add Bonus $ " + request.POST.get(
                'bonus_amount')
            request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')

            return redirect(reverse('New_Bonus'))  # We redirect to the same view

        except EMP_POLICE_VERFICATION.DoesNotExist:
            request.session['New_Client_Req'] = request.POST.get('emp_code') + " is Not Register"
            request.session['New_Client_Code'] = " "

            return render(request, 'add_bonus.html')

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            print("new")
            return render(request, 'add_bonus.html')
        else:
            print("old")
            session_client_name = request.session['New_Client_Req']
            session_client_code = request.session['New_Client_Code']

            del request.session["New_Client_Req"]
            del request.session["New_Client_Code"]
            request.session.modified = True

            return render(request, 'add_bonus.html',
                          {'session_client_name': session_client_name, 'session_client_code': session_client_code})


@login_required(login_url='login')
def new_award(request):
    if request.method == 'POST':
        try:
            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                 'EMP_SAL').get(EMP_CODE=request.POST.get('emp_code'))
            try:
                same_data = EMP_AWARD_LIST.objects.get(EMP_CODE=request.POST.get('emp_code'),
                                                       AWARD_MONTH=request.POST.get('date_month'),
                                                       AWARD_CATEGORY=request.POST.get('new_award'))
                request.session['New_Client_Req'] = "Already Exist Award " + request.POST.get(
                    'new_award')
                request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')

                return redirect(reverse('Award_List'))
            except EMP_AWARD_LIST.DoesNotExist:
                print(data)
                EMP_NAME = data.NEW_EMP.EMP_NAME
                DESIGNATION = data.EMP_COMPANY.DESIGNATION
                DATE = datetime.now().strftime("%Y-%m-%d")
                print(request.POST.get('status'))

                new_award = EMP_AWARD_LIST(
                    EMP_CODE=request.POST.get('emp_code'),
                    EMP_NAME=EMP_NAME,
                    DESIGNATION=DESIGNATION,
                    AWARD_CATEGORY=request.POST.get('new_award'),
                    GIFT=request.POST.get('gift_amount'),
                    AWARD_MONTH=request.POST.get('date_month'),
                    AWARD_DESCRIPTION=request.POST.get('award_description'),
                    AWARD_STATUS=request.POST.get('status'),
                    AWARD_ADD_DATE=DATE,
                )
                new_award.save()

                request.session['New_Client_Req'] = "Successfully Add Award " + request.POST.get(
                    'new_award')
                request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')

                return redirect(reverse('Award_List'))  # We redirect to the same view
        except EMP_POLICE_VERFICATION.DoesNotExist:
            request.session['New_Client_Req'] = request.POST.get('emp_code') + " is Not Register"
            request.session['New_Client_Code'] = " "

            return render(request, 'new_award.html')

        # return render(request, 'new_employee_reg.html', {'message': "Successfully Created Employee",'name':request.POST.get('employee_name')})
    else:
        if 'New_Client_Req' not in request.session:
            data = AWARD_CATEGORY_LIST.objects.filter(STATUS="Published")
            return render(request, 'new_award.html', {'data': data})
        else:
            data = AWARD_CATEGORY_LIST.objects.filter(STATUS="Published")
            session_client_name = request.session['New_Client_Req']
            session_client_code = request.session['New_Client_Code']

            del request.session["New_Client_Req"]
            del request.session["New_Client_Code"]
            request.session.modified = True

            return render(request, 'new_award.html',
                          {'session_client_name': session_client_name, 'session_client_code': session_client_code,
                           'data': data})


@login_required(login_url='login')
def new_notice(request):
    if request.method == 'POST':
        DATE = datetime.now().strftime("%Y-%m-%d")
        add_notice = NOTICE_BOARD(
            TITLE=request.POST.get('title'),
            DESCRIPTION=request.POST.get('notice_description'),
            CREATED_AT=DATE,
            STATUS=request.POST.get('status'),
        )
        add_notice.save()
        request.session['New_Client_Req'] = "Successfully Add Notice " + request.POST.get(
            'title')
        return redirect(reverse('Notice_List'))
    else:
        return render(request, 'add_notice.html')


@login_required(login_url='login')
def add_city(request):
    if request.method == 'POST':
        DATE = datetime.now().strftime("%Y-%m-%d")
        add_notice = NOTICE_BOARD(
            TITLE=request.POST.get('title'),
            DESCRIPTION=request.POST.get('notice_description'),
            CREATED_AT=DATE,
            STATUS=request.POST.get('status'),
        )
        add_notice.save()
        request.session['New_Client_Req'] = "Successfully Add Notice " + request.POST.get(
            'title')
        return redirect(reverse('Notice_List'))
    else:
        country_list = COUNTRY_LIST.objects.all()
        state_list = STATE_LIST.objects.all()

        country = "not_null"
        state = "not_null"

        if not country_list:
            country = "null"
        if not state_list:
            state = "null"
        value = {
            'country': country,
            'country_data_list': country_list,
            'state': state,
            'state_data_list': state_list,
        }
        return render(request, 'add_city.html', value)


@login_required(login_url='login')
def add_client_type(request):
    if request.method == 'POST':
        DATE = datetime.now().strftime("%Y-%m-%d")
        add_client_type = CLIENT_TYPE(
            CLIENT_TYPE=request.POST.get('client_type'),
            DESCRIPTION=request.POST.get('description'),
            CREATED_AT=DATE,
            STATUS=request.POST.get('status'),
        )
        add_client_type.save()
        request.session['New_Client_Req'] = "Successfully Add Client Type " + request.POST.get(
            'client_type')
        return redirect(reverse('Client_Type_List'))


@login_required(login_url='login')
def add_designation(request):
    if request.method == 'POST':
        DATE = datetime.now().strftime("%Y-%m-%d")
        add_client_type = DESIGNATION_LIST(
            DESIGNATION=request.POST.get('designation'),
            DESCRIPTION=request.POST.get('description'),
            CREATED_AT=DATE,
            STATUS=request.POST.get('status'),
        )
        add_client_type.save()
        request.session['New_Client_Req'] = "Successfully Add Designation " + request.POST.get(
            'designation')
        return redirect(reverse('Designation_List'))


@login_required(login_url='login')
def add_event(request):
    if request.method == 'POST':
        DATE = datetime.now().strftime("%Y-%m-%d")
        add_client_type = PERSONAL_EVENT(
            EVENT_NAME=request.POST.get('event_name'),
            START_DATE=request.POST.get('start_date'),
            END_DATE=request.POST.get('end_date'),
            DESCRIPTION=request.POST.get('description'),
            CREATED_AT=DATE,
            STATUS=request.POST.get('status'),
        )
        add_client_type.save()
        request.session['New_Client_Req'] = "Successfully Add Event " + request.POST.get(
            'event_name')
        return redirect(reverse('Event_List'))


@login_required(login_url='login')
def attendance_setting(request):
    if request.method == 'POST':
        cli_count = ATTENDANCE_SETTING.objects.count()
        print(cli_count)
        if cli_count == 0:
            add_client_type = ATTENDANCE_SETTING(
                ATTENDANCE_SETTING=request.POST.get('activate_type'),
            )
            add_client_type.save()
        if cli_count == 1:
            ATTENDANCE_SETTING.objects.filter(ID=request.POST.get('id')).update(
                ATTENDANCE_SETTING=request.POST.get('activate_type'),
            )
        request.session['New_Client_Req'] = "Update Successfully"
        return redirect(reverse('Attendance_Setting'))
    else:
        data = ATTENDANCE_SETTING.objects.all()
        db_value = "not_null"
        if not data:
            db_value = "null"
        if 'New_Client_Req' not in request.session:
            return render(request, 'attendance_setting.html', {'db_value': db_value, 'data': data})
        else:
            session_client_name = request.session['New_Client_Req']

            del request.session["New_Client_Req"]
            request.session.modified = True
            return render(request, 'attendance_setting.html',
                          {'data': data, 'session_client_name': session_client_name, 'db_value': db_value})


@login_required(login_url='login')
def working_day(request):
    if request.method == 'POST':
        db_count = WORKING_DAY.objects.count()
        if db_count == 0:
            sun = 0
            mon = 0
            tue = 0
            wed = 0
            thu = 0
            fri = 0
            sat = 0
            if 'sun' in request.POST:
                sun = "1"
            if 'mon' in request.POST:
                mon = "1"
            if 'tue' in request.POST:
                tue = "1"
            if 'wed' in request.POST:
                wed = "1"
            if 'thu' in request.POST:
                thu = "1"
            if 'fri' in request.POST:
                fri = "1"
            if 'sat' in request.POST:
                sat = "1"
            set_working_day = WORKING_DAY(
                SUNDAY=sun,
                MONDAY=mon,
                TUESDAY=tue,
                WEDNESDAY=wed,
                THURSDAY=thu,
                FRIDAY=fri,
                SATURDAY=sat,
            )
            set_working_day.save()
        if db_count == 1:
            sun = 0
            mon = 0
            tue = 0
            wed = 0
            thu = 0
            fri = 0
            sat = 0
            if 'sun' in request.POST:
                sun = "1"
            if 'mon' in request.POST:
                mon = "1"
            if 'tue' in request.POST:
                tue = "1"
            if 'wed' in request.POST:
                wed = "1"
            if 'thu' in request.POST:
                thu = "1"
            if 'fri' in request.POST:
                fri = "1"
            if 'sat' in request.POST:
                sat = "1"
            print(request.POST.get('id'))
            WORKING_DAY.objects.filter(ID=request.POST.get('id')).update(
                SUNDAY=sun,
                MONDAY=mon,
                TUESDAY=tue,
                WEDNESDAY=wed,
                THURSDAY=thu,
                FRIDAY=fri,
                SATURDAY=sat,
            )
        request.session['New_Client_Req'] = "Update Successfully"
        return redirect(reverse('Set_Working_Day'))
    else:
        data = WORKING_DAY.objects.all()
        db_value = "not_null"
        if not data:
            db_value = "null"
        if 'New_Client_Req' not in request.session:
            return render(request, 'working_day.html', {'db_value': db_value, 'data': data})
        else:
            session_client_name = request.session['New_Client_Req']

            del request.session["New_Client_Req"]
            request.session.modified = True
            return render(request, 'working_day.html',
                          {'data': data, 'session_client_name': session_client_name, 'db_value': db_value})


@login_required(login_url='login')
def add_award_category(request):
    if request.method == 'POST':
        DATE = datetime.now().strftime("%Y-%m-%d")
        add_client_type = AWARD_CATEGORY_LIST(
            AWARD_CATEGORY=request.POST.get('award_name'),
            CREATED_AT=DATE,
            STATUS=request.POST.get('status'),
        )
        add_client_type.save()
        request.session['New_Client_Req'] = "Successfully Add Award Category " + request.POST.get(
            'award_name')
        return redirect(reverse('Award_Category_List'))


@login_required(login_url='login')
def add_holidays(request):
    if request.method == 'POST':
        DATE = datetime.now().strftime("%Y-%m-%d")
        add_holidays = HOLIDAYS(
            HOLIDAY_NAME=request.POST.get('holiday_name'),
            DESCRIPTION=request.POST.get('holiday_description'),
            HOLIDAY_DATE=request.POST.get('holiday_date'),
            STATUS=request.POST.get('status'),
        )
        add_holidays.save()
        request.session['New_Client_Req'] = "Successfully Add Holiday " + request.POST.get(
            'holiday_name')
        return redirect(reverse('Holidays_List'))
    else:
        return render(request, 'add_holidays.html')


@login_required(login_url='login')
def file_management(request):
    if request.method == 'POST':
        try:
            folder = MANAGE_FOLDERS.objects.get(FOLDER_NAME=request.POST.get('folder_name'))
            request.session['New_Client_Req'] = request.POST.get('folder_name') + " is Already Exist"
            request.session['New_Client_Code'] = " "
        except MANAGE_FOLDERS.DoesNotExist:
            DATE = datetime.now().strftime("%Y-%m-%d")
            add_folder = MANAGE_FOLDERS(
                FOLDER_NAME=request.POST.get('folder_name'),
                DESCRIPTION=request.POST.get('folder_description'),
                CREATED_AT=DATE,
            )
            add_folder.save()
            request.session['New_Client_Req'] = "Successfully Create Folder " + request.POST.get(
                'folder_name')
            request.session['New_Client_Code'] = " "
        return redirect(reverse('File_Management'))
    else:
        if 'New_Client_Req' not in request.session:
            data = MANAGE_FOLDERS.objects.all()
            if not data:
                data = "null"
                return render(request, 'file_management.html', {'data': data})
            else:
                data_list = []
                count = 0
                for details in data:
                    count += 1

                    class details_class:
                        ID = count
                        FOLDER_NAME = details.FOLDER_NAME
                        DESCRIPTION = details.DESCRIPTION
                        CREATED_AT = details.CREATED_AT

                    data_list.append(details_class)
                return render(request, 'file_management.html', {'data': data_list})
        else:
            session_client_name = request.session['New_Client_Req']
            session_client_code = request.session['New_Client_Code']

            del request.session["New_Client_Req"]
            del request.session["New_Client_Code"]
            request.session.modified = True
            data = MANAGE_FOLDERS.objects.all()
            if not data:
                data = "null"
                return render(request, 'file_management.html',
                              {'data': data, 'session_client_name': session_client_name,
                               'session_client_code': session_client_code})
            else:
                data_list = []
                count = 0
                for details in data:
                    count += 1

                    class details_class:
                        ID = count
                        FOLDER_NAME = details.FOLDER_NAME
                        DESCRIPTION = details.DESCRIPTION
                        CREATED_AT = details.CREATED_AT

                    data_list.append(details_class)
                return render(request, 'file_management.html',
                              {'data': data_list, 'session_client_name': session_client_name,
                               'session_client_code': session_client_code})


@login_required(login_url='login')
def add_bank(request):
    if request.method == 'POST':
        bank_name = request.POST.get('bank_name')
        if request.POST.get('SUBMIT') == "ADD":
            try:
                folder = BANK_LIST.objects.get(BANK_NAME=bank_name)
                request.session['New_Client_Req'] = "Already Exist File " + bank_name
            except BANK_LIST.DoesNotExist:
                add_folder = BANK_LIST(
                    BANK_NAME=bank_name,
                )
                add_folder.save()
                request.session['New_Client_Req'] = "Successfully Add File " + bank_name
        elif request.POST.get('SUBMIT') == "UPDATE":
            BANK_LIST.objects.filter(ID=request.POST.get('bank_id')).update(
                BANK_NAME=bank_name,
            )
            request.session['New_Client_Req'] = "Your Update is Complete Successfully"
        elif request.POST.get('SUBMIT') == "DELETE":
            BANK_LIST.objects.get(ID=request.POST.get('bank_id')).delete()
            request.session['New_Client_Req'] = "Your Delete is Complete Successfully "
        return redirect(reverse('Add_Bank'))
    else:
        data = BANK_LIST.objects.all()
        if 'New_Client_Req' not in request.session:
            if not data:
                data = "null"
                return render(request, 'add_bank_list.html', {'data': data})
            else:
                return render(request, 'add_bank_list.html', {'data': data})

        else:

            session_client_name = request.session['New_Client_Req']

            del request.session["New_Client_Req"]
            request.session.modified = True
            if not data:
                data = "null"
                return render(request, 'add_bank_list.html', {'data': data, 'session_client_name': session_client_name})
            else:
                return render(request, 'add_bank_list.html', {'data': data, 'session_client_name': session_client_name})


@login_required(login_url='login')
def add_file(request):
    if request.method == 'POST':
        upload_file = request.FILES['file_name']
        try:
            folder = MANAGE_FILES.objects.get(UPLOAD_FILE=request.FILES['file_name'],
                                              FOLDER_NAME=request.POST.get('folder_name'))
            request.session['New_Client_Req'] = "Already Exist File " + str(request.FILES['file_name'])
            request.session['New_Client_Code'] = "Folder Name: " + request.POST.get('folder_name')
        except MANAGE_FILES.DoesNotExist:
            profile_img = file_upload(upload_file, request.POST.get('folder_name'))
            DATE = datetime.now().strftime("%Y-%m-%d")
            add_folder = MANAGE_FILES(
                FOLDER_NAME=request.POST.get('folder_name'),
                CAPTION=request.POST.get('caption'),
                UPLOAD_FILE=request.FILES['file_name'],
                UPLOAD_FILE_URL=profile_img,
                CREATED_AT=DATE,
            )
            add_folder.save()
            request.session['New_Client_Req'] = "Successfully Add File " + str(request.FILES['file_name'])
            request.session['New_Client_Code'] = "Folder Name: " + request.POST.get('folder_name')
        return redirect(reverse('File_Management'))
    else:
        folder_name = request.GET.get('folder_name')
        print(folder_name)
        data = MANAGE_FILES.objects.filter(FOLDER_NAME=request.GET.get('folder_name')).all()
        if not data:
            data = "null"
            return render(request, 'add_file.html', {'data': data, 'folder_name': folder_name})
        else:
            data_list = []
            count = 0
            for details in data:
                count += 1

                class details_class:
                    ID = count
                    FOLDER_NAME = details.FOLDER_NAME
                    CAPTION = details.CAPTION
                    UPLOAD_FILE = details.UPLOAD_FILE
                    CREATED_AT = details.CREATED_AT

                data_list.append(details_class)
            return render(request, 'add_file.html', {'data': data_list, 'folder_name': folder_name})


@login_required(login_url='login')
def delete_file(request):
    if request.method == 'POST':
        MANAGE_FILES.objects.get(UPLOAD_FILE=request.POST.get('file_name'),
                                 FOLDER_NAME=request.POST.get('folder_name')).delete()
        file_delete(request.POST.get('file_name'), request.POST.get('folder_name'))
        request.session['New_Client_Req'] = "Successfully Delete File " + request.POST.get('file_name')
        request.session['New_Client_Code'] = "Folder Name: " + request.POST.get('folder_name')
        return redirect(reverse('File_Management'))


@login_required(login_url='login')
def download_file(request):
    value = request.GET.get('folder_name').split('~')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = value[0]
    filepath = base_dir + '/templates/media' + "/" + value[1] + "/" + filename
    filename = os.path.basename(filepath)
    response = HttpResponse(open(filepath, 'rb'), content_type=mimetypes.guess_type(filepath))
    response['Content-Disposition'] = "attachment;filename=%s" % filename
    return response


@login_required(login_url='login')
def edit_bonus(request):
    if request.method == "POST":
        print("yes post update", request.POST.get('emp_code'))
        EMP_BONUS_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_code')).update(
            BONUS_NAME=request.POST.get('bonus_name'),
            BONUS_AMOUNT=request.POST.get('bonus_amount'),
            BONUS_DESCRIPTION=request.POST.get('bonus_description'),
            BONUS_UPDATE_DATE=request.POST.get('date_month'),
        )
        emp_code = EMP_BONUS_DETAILS.objects.all()
        return redirect(reverse('New_Bonus'), {'data': emp_code})
    else:
        emp_code = request.GET.get('secure')
        if emp_code is not None:
            print(emp_code)
            emp_code = EMP_BONUS_DETAILS.objects.filter(EMP_CODE=emp_code)
            print(request.GET.get('secure'))

            return render(request, 'edit_bonus.html', {'data': emp_code})
        else:
            print(emp_code)
            return render(request, 'edit_bonus.html')


@login_required(login_url='login')
def edit_expense_category(request):
    if request.method == "POST":
        error_messege = ""
        try:
            data = EXPENSE_CATEGORY_LIST.objects.get(EXP_PURPOSE=request.POST.get('purpose_name'))
            error_messege = request.POST.get('purpose_name') + " is Already Exist"
            error_count = "1"
            print("try")
        except EXPENSE_CATEGORY_LIST.DoesNotExist:
            print("catch!")
            error_count = "0"
            EXPENSE_CATEGORY_LIST.objects.filter(ID=request.POST.get('purpose_id')).update(
                EXP_PURPOSE=request.POST.get('purpose_name'),
            )
        data = EXPENSE_CATEGORY_LIST.objects.all()
        data_list = []
        count = 0
        for details in data:
            count += 1

            class details_class:
                ID = count
                EXP_PURPOSE = details.EXP_PURPOSE
                CREATED_BY = details.CREATED_BY

            data_list.append(details_class)
        print(error_messege)
        print(error_count)
        return render(request, 'expense_category_list.html',
                      {'data': data_list, 'error': error_messege, 'err_count': error_count})
    else:
        emp_code = request.GET.get('secure')
        if emp_code is not None:
            print(emp_code)
            emp_code = EXPENSE_CATEGORY_LIST.objects.filter(EXP_PURPOSE=emp_code)
            return render(request, 'edit_expense_category.html', {'data': emp_code})
        else:
            print(emp_code)
            return redirect(reverse('Expense_Category_List'))


@login_required(login_url='login')
def edit_leave_category(request):
    if request.method == "POST":
        error_messege = ""
        id_detail = LEAVE_CATEGORY_LIST.objects.get(ID=request.POST.get('leave_id'))

        CATEGORY_NAME = id_detail.CATEGORY_NAME

        print(CATEGORY_NAME, "name")
        if CATEGORY_NAME == request.POST.get('leave_name'):
            error_count = "0"
            LEAVE_CATEGORY_LIST.objects.filter(ID=request.POST.get('leave_id')).update(
                CATEGORY_NAME=request.POST.get('leave_name'),
                CATEGORY_DESCRIPTION=request.POST.get('category_description'),
                STATUS=request.POST.get('status'),
            )
        else:
            try:
                data = LEAVE_CATEGORY_LIST.objects.get(CATEGORY_NAME=request.POST.get('leave_name'))
                error_messege = request.POST.get('leave_name') + " is Already Exist"
                error_count = "1"
                print("try")
            except LEAVE_CATEGORY_LIST.DoesNotExist:
                print("catch!")
                error_count = "0"
                LEAVE_CATEGORY_LIST.objects.filter(ID=request.POST.get('leave_id')).update(
                    CATEGORY_NAME=request.POST.get('leave_name'),
                    CATEGORY_DESCRIPTION=request.POST.get('category_description'),
                    STATUS=request.POST.get('status'),
                )
        data = LEAVE_CATEGORY_LIST.objects.all()
        data_list = []
        count = 0
        for details in data:
            count += 1

            class details_class:
                ID = count
                CATEGORY_NAME = details.CATEGORY_NAME
                CATEGORY_DESCRIPTION = details.CATEGORY_DESCRIPTION
                STATUS = details.STATUS
                ADDED_DATE = details.ADDED_DATE

            data_list.append(details_class)
        print(error_messege)
        print(error_count)
        return render(request, 'leave_category_list.html',
                      {'data': data_list, 'error': error_messege, 'err_count': error_count})
    else:
        emp_code = request.GET.get('secure')
        if emp_code is not None:
            print(emp_code)
            emp_code = LEAVE_CATEGORY_LIST.objects.filter(CATEGORY_NAME=emp_code)
            return render(request, 'edit_leave_category.html', {'data': emp_code})
        else:
            print(emp_code)
            return redirect(reverse('Leave_Category_List'))


@login_required(login_url='login')
def edit_certificate(request):
    if request.method == "POST":
        EMP_CERTIFICATE_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_code'),
                                               CERTIFICATE_TYPE=request.POST.get('certificate_type')).update(
            CERTIFICATE_DESCRIPTION=request.POST.get('certificate_description'),
        )
        request.session['New_Client_Req'] = request.POST.get(
            'certificate_type') + " Certificate is Successfully Updated"
        return redirect(reverse('Certificate_List'))
    else:
        emp_code = request.GET.get('secure')
        if emp_code is not None:
            emp_code = request.GET.get('secure').split('~')
            print(emp_code)
            data = EMP_CERTIFICATE_DETAILS.objects.filter(EMP_CODE=emp_code[0], CERTIFICATE_TYPE=emp_code[1])
            return render(request, 'edit_certificate.html', {'data': data})
        else:
            print(emp_code)
            return redirect(reverse('Certificate_List'))


@login_required(login_url='login')
def edit_award(request):
    if request.method == "POST":
        id_detail = EMP_AWARD_LIST.objects.get(ID=request.POST.get('db_id'))

        AWARD_CATEGORY = id_detail.AWARD_CATEGORY
        AWARD_MONTH = id_detail.AWARD_MONTH

        if AWARD_CATEGORY == request.POST.get('new_award') and AWARD_MONTH == request.POST.get('date_month'):
            EMP_AWARD_LIST.objects.filter(ID=request.POST.get('db_id')).update(
                AWARD_CATEGORY=request.POST.get('new_award'),
                GIFT=request.POST.get('gift_amount'),
                AWARD_MONTH=request.POST.get('date_month'),
                AWARD_DESCRIPTION=request.POST.get('award_description'),
                AWARD_STATUS=request.POST.get('status'),
            )
            request.session['New_Client_Req'] = " Data is Successfully Updated"
            request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')
        else:
            try:
                data = EMP_AWARD_LIST.objects.get(EMP_CODE=request.POST.get('emp_code'),
                                                  AWARD_MONTH=request.POST.get('date_month'),
                                                  AWARD_CATEGORY=request.POST.get('new_award'))
                request.session['New_Client_Req'] = "Already Exist Award " + request.POST.get(
                    'new_award')
                request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')
            except EMP_AWARD_LIST.DoesNotExist:
                EMP_AWARD_LIST.objects.filter(ID=request.POST.get('db_id')).update(
                    AWARD_CATEGORY=request.POST.get('new_award'),
                    GIFT=request.POST.get('gift_amount'),
                    AWARD_MONTH=request.POST.get('date_month'),
                    AWARD_DESCRIPTION=request.POST.get('award_description'),
                    AWARD_STATUS=request.POST.get('status'),
                )
                request.session['New_Client_Req'] = " Data is Successfully Updated"
                request.session['New_Client_Code'] = " Employee Code : " + request.POST.get('emp_code')

        return redirect(reverse('Award_List'))
    else:
        emp_code = request.GET.get('secure')
        if emp_code is not None:
            emp_code = request.GET.get('secure').split('~')
            print(emp_code)
            data = EMP_AWARD_LIST.objects.filter(EMP_CODE=emp_code[0], AWARD_MONTH=emp_code[1],
                                                 AWARD_CATEGORY=emp_code[2])
            return render(request, 'edit_award.html', {'data': data})
            print(emp_code)
        else:
            return redirect(reverse('Award_List'))


@login_required(login_url='login')
def edit_leave_application(request):
    if request.method == "GET":
        approval = request.GET.get('value')
        if approval is not None:
            approval = request.GET.get('value').split('~')
            if approval[0] == "Accepted":
                LEAVE_APPLICATION_LIST.objects.filter(EMP_CODE=approval[1], START_DATE=approval[2]).update(
                    STATUS="Accepted",
                )
                return redirect(reverse('Leave_Application_List'))
            elif approval[0] == "Rejected":
                LEAVE_APPLICATION_LIST.objects.filter(EMP_CODE=approval[1], START_DATE=approval[2]).update(
                    STATUS="Rejected",
                )
                return redirect(reverse('Leave_Application_List'))

        else:
            print(emp_code)
            return redirect(reverse('Leave_Application_List'))


@login_required(login_url='login')
def edit_notice_status(request):
    if request.method == "GET":
        status = request.GET.get('value').split('~')
        if status[0] == "Published":
            NOTICE_BOARD.objects.filter(ID=status[1]).update(
                STATUS="Published",
            )
        elif status[0] == "Unpublished":
            NOTICE_BOARD.objects.filter(ID=status[1]).update(
                STATUS="Unpublished",
            )
        return redirect(reverse('Notice_List'))


@login_required(login_url='login')
def edit_holiday_status(request):
    if request.method == "GET":
        status = request.GET.get('value').split('~')
        if status[0] == "Published":
            HOLIDAYS.objects.filter(ID=status[1]).update(
                STATUS="Published",
            )
        elif status[0] == "Unpublished":
            HOLIDAYS.objects.filter(ID=status[1]).update(
                STATUS="Unpublished",
            )
        return redirect(reverse('Holidays_List'))


@login_required(login_url='login')
def edit_expense(request):
    if request.method == "POST":
        EMP_EXPENSE_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_code')).update(
            EXPENSE_DATE=request.POST.get('expense_date'),
            EXPENSE_AMOUNT=request.POST.get('expense_amount'),
            EXPENSE_PURPOSE=request.POST.get('expense_purpose'),
            REMARK=request.POST.get('remark'),
        )
        return redirect(reverse('Expense_List'))
    else:
        emp_code = request.GET.get('secure')
        if emp_code is not None:
            print(emp_code)
            emp_code = EMP_EXPENSE_DETAILS.objects.filter(EMP_CODE=emp_code)
            print(request.GET.get('secure'))
            return render(request, 'edit_expense.html', {'data': emp_code})
        else:
            print(emp_code)
            return render(request, 'edit_expense.html')


@login_required(login_url='login')
def edit_loan(request):
    if request.method == "POST":
        EMP_LOAN_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_code')).update(
            LOAN_NAME=request.POST.get('loan_name'),
            LOAN_AMOUNT=request.POST.get('loan_amount'),
            AMOUNT_OF_INSTALLMENT=request.POST.get('amount_of_inst'),
            LOAN_DESCRIPTION=request.POST.get('loan_description'),
            REMAINING_OF_INSTALLMENT=request.POST.get('remin_of_inst'),
        )
        emp_code = EMP_BONUS_DETAILS.objects.all()
        return redirect(reverse('Loan_List'), {'data': emp_code})
    else:
        emp_code = request.GET.get('secure')
        if emp_code is not None:
            print(emp_code)
            emp_code = EMP_LOAN_DETAILS.objects.filter(EMP_CODE=emp_code)
            print(request.GET.get('secure'))
            return render(request, 'edit_loan.html', {'data': emp_code})
        else:
            print(emp_code)
            return render(request, 'edit_loan.html')


@login_required(login_url='login')
def manage_customer_register(request):
    emp_code = New_Customer_Reg.objects.all()
    return render(request, 'manage_client.html', {'data': emp_code})


@login_required(login_url='login')
def client_view(request):
    emp_code = request.GET.get('secure')
    print(emp_code)
    emp_code = New_Customer_Reg.objects.get(CLIENT_NAME=emp_code)
    emp_db_code = emp_code.CLIENT_NAME
    em_mon_report = []
    print(request.GET.get('secure'))

    class details_class:
        CLIENT_NAME = emp_code.CLIENT_NAME
        CLIENT_CODE = emp_code.CLIENT_CODE
        EMAIL = emp_code.EMAIL
        DOB = emp_code.DOB
        CONTACT_NO = emp_code.CONTACT_NO
        GENTER = emp_code.GENTER
        EMERGENCY_CONTACT_NO = emp_code.EMERGENCY_CONTACT_NO
        ADDRESS = emp_code.ADDRESS
        CLIENT_TYPE = emp_code.CLIENT_TYPE
        JOIN_DATE = emp_code.REG_DATE

    em_mon_report.append(details_class)
    return render(request, 'client_view.html', {'data': em_mon_report, 'client_id': emp_code})


@login_required(login_url='login')
def loan_view(request):
    if request.method == "GET":
        emp_code = request.GET.get('secure')
        emp_code = EMP_LOAN_DETAILS.objects.filter(EMP_CODE=emp_code)
        return render(request, 'view_loan.html', {'data': emp_code})


@login_required(login_url='login')
def employee_salary_list1(request):
    if 'UPDATE_EMP_SALARY_DETAILS' not in request.session:
        data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                             'EMP_SAL').all()
        count = 0
        em_mon_report = []
        for details in data:
            count += 1

            class details_class:
                id = count
                EMP_NAME = details.NEW_EMP.EMP_NAME
                EMP_CODE = details.NEW_EMP.EMP_CODE
                DESIGNATION = details.EMP_COMPANY.DESIGNATION
                TOTAL_EARN = details.EMP_SAL.TOTAL_EARN
                TOTAL_DEDUCATION = details.EMP_SAL.TOTAL_DEDUCATION
                NET_PAY = details.EMP_SAL.NET_PAY
                SALARY_UPDATE_DATE = details.EMP_SAL.SALARY_UPDATE_DATE
                ext = SALARY_UPDATE_DATE
                print(ext)
                if ext == "NO UPDATED":
                    print = details.EMP_CODE + "~" + ext + "~" + details.EMP_COMPANY.DESIGNATION + "~" + details.NEW_EMP.EMP_NAME
                else:
                    ext = SALARY_UPDATE_DATE.split("-")
                    print = details.EMP_CODE + "~" + ext[1] + "~" + ext[0] + "~" + details.EMP_COMPANY.DESIGNATION

            em_mon_report.append(details_class)
        return render(request, 'employee_salary_details.html', {'data': em_mon_report})
    else:
        data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                             'EMP_SAL').all()
        count = 0
        em_mon_report = []
        for details in data:
            count += 1

            class details_class:
                id = count
                EMP_NAME = details.NEW_EMP.EMP_NAME
                EMP_CODE = details.NEW_EMP.EMP_CODE
                DESIGNATION = details.EMP_COMPANY.DESIGNATION
                TOTAL_EARN = details.EMP_SAL.TOTAL_EARN
                TOTAL_DEDUCATION = details.EMP_SAL.TOTAL_DEDUCATION
                NET_PAY = details.EMP_SAL.NET_PAY
                SALARY_UPDATE_DATE = details.EMP_SAL.SALARY_UPDATE_DATE
                ext = SALARY_UPDATE_DATE
                print(type(ext))
                if ext == "NO UPDATED":
                    print = details.EMP_CODE + "~" + ext + "~" + details.EMP_COMPANY.DESIGNATION + "~" + details.NEW_EMP.EMP_NAME
                else:
                    ext = SALARY_UPDATE_DATE.split("-")
                    print = details.EMP_CODE + "~" + ext[1] + "~" + ext[0] + "~" + details.EMP_COMPANY.DESIGNATION

            em_mon_report.append(details_class)
        update_messages = request.session['UPDATE_EMP_SALARY_DETAILS']
        del request.session["UPDATE_EMP_SALARY_DETAILS"]

        request.session.modified = True

        return render(request, 'employee_salary_details.html',
                      {'data': em_mon_report, 'update_messages': update_messages})


@login_required(login_url='login')
def employee_salary_list(request):
    if request.method == "POST":
        client_list = []
        report_array = []
        country_list = []
        client = CLIENT_DETAILS.objects.all()
        for i in range(len(client)):
            variable = client[i].CLIENT
            print(variable)
            if variable not in client_list:
                client_list.append(variable)
        filter_client = request.POST.get('client')
        result_set = []
        filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=filter_client)
        for client_details in filter_client_list:
            result_set.append(client_details)

        for i in range(len(result_set)):
            country = result_set[i].COUNTRY_NAME
            if country not in country_list:
                country_list.append(country)
        form = request.POST
        filter_value = "no"
        data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                             'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client)

        for emp_details in data:
            EMP_CODE = emp_details.NEW_EMP.EMP_CODE
            print(EMP_CODE)
            employer_details = salary_details.objects.filter(EMP_CODE=EMP_CODE)
            for details in employer_details:
                filter_value = "yes"

                class details_class:
                    EMP_NAME = emp_details.NEW_EMP.EMP_NAME
                    EMP_CODE = emp_details.NEW_EMP.EMP_CODE
                    DESIGNATION = emp_details.EMP_COMPANY.DESIGNATION
                    TOTAL_EARN = details.TOTAL_EARN
                    TOTAL_DEDUCATION = details.TOTAL_DEDUCATION
                    NET_PAY = details.NET_PAY
                    SALARY_UPDATE_DATE = details.SALARY_UPDATE_DATE
                    ext = SALARY_UPDATE_DATE
                    print(type(ext))
                    if ext == "NO UPDATED":
                        print = details.EMP_CODE + "~" + ext + "~" + emp_details.EMP_COMPANY.DESIGNATION + "~" + emp_details.NEW_EMP.EMP_NAME
                    else:
                        ext = SALARY_UPDATE_DATE.split("-")
                        print = details.EMP_CODE + "~" + ext[1] + "~" + ext[
                            0] + "~" + emp_details.EMP_COMPANY.DESIGNATION

                report_array.append(details_class)

        dummy_value = request.POST.get('client')
        # wage_de = Form_B_Obj(client, unit, month, year)
        value = {
            'data': report_array,
            'client': client_list,
            'country_list': country_list,
            'filter_value': filter_value,
            'dummy_value': dummy_value,
        }

        return render(request, 'employee_salary_details.html', value)

    else:
        if request.GET.get('client') is None:
            client_list = []
            client = CLIENT_DETAILS.objects.all()
            for i in range(len(client)):
                variable = client[i].CLIENT
                print(variable)
                if variable not in client_list:
                    client_list.append(variable)
            if 'UPDATE_EMP_SALARY_DETAILS' not in request.session:
                value = {
                    'client': client_list,
                }
            else:
                update_messages = request.session['UPDATE_EMP_SALARY_DETAILS']
                print("esdesldsldkl")
                del request.session["UPDATE_EMP_SALARY_DETAILS"]

                request.session.modified = True

                value = {
                    'client': client_list,
                    'update_messages': update_messages,
                }
        else:
            get_value = request.GET.get('client')
            client_list = []
            report_array = []
            country_list = []
            client = CLIENT_DETAILS.objects.all()
            for i in range(len(client)):
                variable = client[i].CLIENT
                print(variable)
                if variable not in client_list:
                    client_list.append(variable)
            result_set = []
            filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=get_value)
            for client_details in filter_client_list:
                result_set.append(client_details)

            for i in range(len(result_set)):
                country = result_set[i].COUNTRY_NAME
                if country not in country_list:
                    country_list.append(country)
            form = request.POST
            filter_value = "no"
            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=get_value)

            for emp_details in data:
                EMP_CODE = emp_details.NEW_EMP.EMP_CODE
                print(EMP_CODE)
                employer_details = salary_details.objects.filter(EMP_CODE=EMP_CODE)
                for details in employer_details:
                    filter_value = "yes"

                    class details_class:
                        EMP_NAME = emp_details.NEW_EMP.EMP_NAME
                        EMP_CODE = emp_details.NEW_EMP.EMP_CODE
                        DESIGNATION = emp_details.EMP_COMPANY.DESIGNATION
                        TOTAL_EARN = details.TOTAL_EARN
                        TOTAL_DEDUCATION = details.TOTAL_DEDUCATION
                        NET_PAY = details.NET_PAY
                        SALARY_UPDATE_DATE = details.SALARY_UPDATE_DATE
                        ext = SALARY_UPDATE_DATE
                        print(type(ext))
                        if ext == "NO UPDATED":
                            print = details.EMP_CODE + "~" + ext + "~" + emp_details.EMP_COMPANY.DESIGNATION + "~" + emp_details.NEW_EMP.EMP_NAME
                        else:
                            ext = SALARY_UPDATE_DATE.split("-")
                            print = details.EMP_CODE + "~" + ext[1] + "~" + ext[
                                0] + "~" + emp_details.EMP_COMPANY.DESIGNATION

                    report_array.append(details_class)

            dummy_value = get_value
            # wage_de = Form_B_Obj(client, unit, month, year)
            value = {
                'data': report_array,
                'client': client_list,
                'country_list': country_list,
                'filter_value': filter_value,
                'dummy_value': dummy_value,
            }
        return render(request, 'employee_salary_details.html', value)


@login_required(login_url='login')
def fiter_emp_salary_list(request):
    if request.method == "POST":
        client_list = []
        country_list = []
        report_array = []
        filter_client = request.POST.get('client_name')
        client = CLIENT_DETAILS.objects.all()
        form_a_filter = ""
        for i in range(len(client)):
            variable = client[i].CLIENT
            print(variable, "variable")
            if variable not in client_list:
                client_list.append(variable)
        filter_value = "yes"
        result_set = []
        filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=filter_client)
        for client_details in filter_client_list:
            result_set.append(client_details)

        for i in range(len(result_set)):
            country = result_set[i].COUNTRY_NAME
            if country not in country_list:
                country_list.append(country)
        if request.POST.get('submit') == "Country":
            form_a_filter = "Country" + "~" + filter_client + "~" + request.POST.get('country_name')
            country_name = request.POST.get('country_name')
            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name)
        elif request.POST.get('submit') == "State":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            form_a_filter = "State" + "~" + filter_client + "~" + country_name + "~" + state_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name)
        elif request.POST.get('submit') == "District":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            form_a_filter = "District" + "~" + filter_client + "~" + country_name + "~" + state_name + "~" + district_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name)
        elif request.POST.get('submit') == "Branch":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            branch_name = request.POST.get('branch_name')
            form_a_filter = "Branch" + "~" + filter_client + "~" + country_name + "~" + state_name + "~" + district_name + "~" + branch_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name,
                                                                                   EMP_COMPANY__BRANCH=branch_name)
        elif request.POST.get('submit') == "Area":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            branch_name = request.POST.get('branch_name')
            area_name = request.POST.get('area_name')
            form_a_filter = "Branch" + "~" + filter_client + "~" + country_name + "~" + state_name + "~" + district_name + "~" + branch_name + "~" + area_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name,
                                                                                   EMP_COMPANY__BRANCH=branch_name,
                                                                                   EMP_COMPANY__AREA=area_name)
        elif request.POST.get('submit') == "Unit":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            branch_name = request.POST.get('branch_name')
            area_name = request.POST.get('area_name')
            unit = request.POST.get('unit_name')
            form_a_filter = "Unit" + "~" + filter_client + "~" + country_name + "~" + state_name + "~" + district_name + "~" + branch_name + "~" + area_name + "~" + unit

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name,
                                                                                   EMP_COMPANY__BRANCH=branch_name,
                                                                                   EMP_COMPANY__AREA=area_name,
                                                                                   EMP_COMPANY__UNIT=unit)
        for emp_details in data:
            EMP_CODE = emp_details.NEW_EMP.EMP_CODE
            employer_details = EMP_SALARY_MAINTAINS.objects.filter(EMP_CODE=EMP_CODE)
            for details in employer_details:
                filter_value = "yes"

                class details_class:
                    EMP_NAME = emp_details.NEW_EMP.EMP_NAME
                    EMP_CODE = emp_details.NEW_EMP.EMP_CODE
                    DESIGNATION = emp_details.EMP_COMPANY.DESIGNATION
                    TOTAL_EARN = details.TOTAL_EARN
                    TOTAL_DEDUCATION = details.TOTAL_DEDUCATION
                    NET_PAY = details.NET_PAY
                    SALARY_UPDATE_DATE = details.SALARY_UPDATE_DATE
                    ext = SALARY_UPDATE_DATE
                    print(type(ext))
                    if ext == "NO UPDATED":
                        print = details.EMP_CODE + "~" + ext + "~" + emp_details.EMP_COMPANY.DESIGNATION + "~" + emp_details.NEW_EMP.EMP_NAME
                    else:
                        ext = SALARY_UPDATE_DATE.split("-")
                        print = details.EMP_CODE + "~" + ext[1] + "~" + ext[
                            0] + "~" + emp_details.EMP_COMPANY.DESIGNATION

                report_array.append(details_class)
        value = {
            'data': report_array,
            'client': client_list,
            'error_message': data,
            'country_list': country_list,
            'filter_value': filter_value,
            'dummy_value': filter_client,
            'form_a_filter': form_a_filter,
        }
        return render(request, 'employee_salary_details.html', value)
    else:
        if request.GET.get('client') is None:
            return redirect(reverse('Employee_Salary_Details'))
        else:
            get_value = request.GET.get('client').split('~')
            client_list = []
            country_list = []
            report_array = []
            filter_client = get_value[1]
            client = CLIENT_DETAILS.objects.all()
            form_a_filter = ""
            for i in range(len(client)):
                variable = client[i].CLIENT
                if variable not in client_list:
                    client_list.append(variable)
            filter_value = "yes"
            result_set = []
            filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=filter_client)
            for client_details in filter_client_list:
                result_set.append(client_details)

            for i in range(len(result_set)):
                country = result_set[i].COUNTRY_NAME
                if country not in country_list:
                    country_list.append(country)
            if get_value[0] == "Country":
                form_a_filter = "Country" + "~" + get_value[1] + "~" + get_value[2]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2])
            elif get_value[0] == "State":
                form_a_filter = "State" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3])
            elif get_value[0] == "District":
                form_a_filter = "District" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + \
                                get_value[4]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3],
                    EMP_COMPANY__DISTRICT=get_value[4])
            elif get_value[0] == "Branch":
                form_a_filter = "Branch" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + \
                                get_value[4] + "~" + get_value[5]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3],
                    EMP_COMPANY__DISTRICT=get_value[4],
                    EMP_COMPANY__BRANCH=get_value[5])
            elif get_value[0] == "Area":
                form_a_filter = "Area" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + get_value[
                    4] + "~" + get_value[5] + "~" + get_value[6]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3],
                    EMP_COMPANY__DISTRICT=get_value[4],
                    EMP_COMPANY__BRANCH=get_value[5],
                    EMP_COMPANY__AREA=get_value[6])
            elif get_value[0] == "Unit":
                form_a_filter = "Unit" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + get_value[
                    4] + "~" + get_value[5] + "~" + get_value[6] + "~" + get_value[7]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3],
                    EMP_COMPANY__DISTRICT=get_value[4],
                    EMP_COMPANY__BRANCH=get_value[5],
                    EMP_COMPANY__AREA=get_value[6],
                    EMP_COMPANY__UNIT=get_value[7])
            for emp_details in data:
                EMP_CODE = emp_details.NEW_EMP.EMP_CODE
                employer_details = EMP_SALARY_MAINTAINS.objects.filter(EMP_CODE=EMP_CODE)
                for details in employer_details:
                    filter_value = "yes"

                    class details_class:
                        EMP_NAME = emp_details.NEW_EMP.EMP_NAME
                        EMP_CODE = emp_details.NEW_EMP.EMP_CODE
                        DESIGNATION = emp_details.EMP_COMPANY.DESIGNATION
                        TOTAL_EARN = details.TOTAL_EARN
                        TOTAL_DEDUCATION = details.TOTAL_DEDUCATION
                        NET_PAY = details.NET_PAY
                        SALARY_UPDATE_DATE = details.SALARY_UPDATE_DATE
                        ext = SALARY_UPDATE_DATE
                        print(type(ext))
                        if ext == "NO UPDATED":
                            print = details.EMP_CODE + "~" + ext + "~" + emp_details.EMP_COMPANY.DESIGNATION + "~" + emp_details.NEW_EMP.EMP_NAME
                        else:
                            ext = SALARY_UPDATE_DATE.split("-")
                            print = details.EMP_CODE + "~" + ext[1] + "~" + ext[
                                0] + "~" + emp_details.EMP_COMPANY.DESIGNATION

                    report_array.append(details_class)
            value = {
                'data': report_array,
                'client': client_list,
                'error_message': data,
                'country_list': country_list,
                'filter_value': filter_value,
                'dummy_value': filter_client,
                'form_a_filter': form_a_filter,
            }
            return render(request, 'employee_salary_details.html', value)


@login_required(login_url='login')
def edit_employee_details(request):
    if request.method == "POST":
        if request.POST.get("GetData") == "GetData":

            if request.POST.get('search_type') == "emp_no":
                emp_code = request.POST.get('emp_code')
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(EMP_CODE=emp_code)
                return render(request, 'Employee_detail_edit.html', {'data': data, 'error_message': data})
            else:
                emp_code = find_emp_code(request.POST.get('emp_code'))
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(EMP_CODE=emp_code)
                return render(request, 'Employee_detail_edit.html', {'data': data, 'error_message': data})
        else:
            if request.POST.get("GetData") == "UPDATE":

                img_file = "false"
                img_doc = "false"
                update_count = 0
                upload_file = ""
                upload_img = ""

                print(request.POST)

                if request.POST.get('docfile') == '':
                    img_doc = "true"
                """
                elif 'docfile' not in request.POST:
                    upload_file = request.FILES['docfile']
                    update_count += update_count
                else:
                    upload_file = request.FILES['docfile']
                    update_count += update_count

                if request.POST.get('imgfile') == '':
                    img_file = "true"
                """
                if request.POST.get('imgfile') == '':
                    img_file = "true"
                """elif 'imgfile' not in request.POST:

                    upload_img = request.FILES['imgfile']
                    update_count += update_count
                else:
                    upload_img = request.FILES['imgfile']
                    update_count += update_count """

                profile_img = ""
                doc_img = ""
                if img_file == "false" or img_doc == "false":
                    if img_file == "false":
                        upload_img = request.FILES['imgfile']
                        profile_img = img_upload(upload_img, "image_upload", request.POST.get('emp_hidden_code'))
                    else:
                        profile_img = img_doc_db_url("img_get", request.POST.get('emp_hidden_code'))

                    if img_doc == "false":
                        upload_file = request.FILES['docfile']
                        doc_img = img_upload(upload_file, "doc_upload", request.POST.get('emp_hidden_code'))
                    else:
                        doc_img = img_doc_db_url("doc_get", request.POST.get('emp_hidden_code'))
                else:
                    profile_img, doc_img = img_doc_db_url("all_get", request.POST.get('emp_hidden_code'))

                EMP_PERSONAL_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(

                    BLOOD_GROUP=request.POST.get('blood_group'),
                    SHOE_SIZE=request.POST.get('shoe_size'),
                    WAIST=request.POST.get('waist'),
                    HEIGHT=request.POST.get('height'),
                    WEIGHT=request.POST.get('weight'),
                    CHEST=request.POST.get('chest'),
                    T_SHIRT_SIZE=request.POST.get('t_shirt'),
                    THOUSER_SIZE=request.POST.get('thouser_size'),
                    DOCUMENT_URL=doc_img,
                    PROFILE_URL=profile_img
                )
                request.session['UPDATE_EMP_PERSONAL_DETAILS'] = "SUCCESSFULLY UPDATED : " + request.POST.get(
                    'emp_hidden_code')
                return redirect(reverse('Employee_Edit'))  # We redirect to the same view
                # return render(request, 'Employee_Edit.html', {'name': "no_file"})
    else:
        if 'UPDATE_EMP_PERSONAL_DETAILS' not in request.session:
            return render(request, 'Employee_detail_edit.html')
        else:
            update_messages = request.session['UPDATE_EMP_PERSONAL_DETAILS']
            del request.session["UPDATE_EMP_PERSONAL_DETAILS"]

            request.session.modified = True

            return render(request, 'Employee_detail_edit.html',
                          {'update_messages': update_messages})


@login_required(login_url='login')
def edit_client_type(request):
    if request.method == "POST":
        if request.POST.get('Edit') == "UPDATE":
            CLIENT_TYPE.objects.filter(ID=request.POST.get('id')).update(
                CLIENT_TYPE=request.POST.get('client_type'),
                DESCRIPTION=request.POST.get('description'),
                STATUS=request.POST.get('status'),
            )
            request.session['New_Client_Req'] = "Your Update is Complete Successfully "
            return redirect(reverse('Client_Type_List'))
        else:
            CLIENT_TYPE.objects.get(ID=request.POST.get('id')).delete()
            request.session['New_Client_Req'] = "Your Delete is Complete Successfully "
            return redirect(reverse('Client_Type_List'))


@login_required(login_url='login')
def edit_designation(request):
    if request.method == "POST":
        if request.POST.get('Edit') == "UPDATE":
            print(request.POST.get('description'))
            DESIGNATION_LIST.objects.filter(ID=request.POST.get('id')).update(
                DESIGNATION=request.POST.get('designation'),
                STATUS=request.POST.get('status'),
            )
            request.session['New_Client_Req'] = "Your Update is Complete Successfully "
            return redirect(reverse('Designation_List'))
        else:
            DESIGNATION_LIST.objects.get(ID=request.POST.get('id')).delete()
            request.session['New_Client_Req'] = "Your Delete is Complete Successfully "
            return redirect(reverse('Designation_List'))


@login_required(login_url='login')
def edit_event(request):
    if request.method == "POST":
        if request.POST.get('Edit') == "UPDATE":
            PERSONAL_EVENT.objects.filter(ID=request.POST.get('id')).update(
                EVENT_NAME=request.POST.get('event_name'),
                START_DATE=request.POST.get('start_date'),
                END_DATE=request.POST.get('end_date'),
                DESCRIPTION=request.POST.get('description'),
                STATUS=request.POST.get('status'),
            )
            request.session['New_Client_Req'] = "Your Update is Complete Successfully "
            return redirect(reverse('Event_List'))
        else:
            PERSONAL_EVENT.objects.get(ID=request.POST.get('id')).delete()
            request.session['New_Client_Req'] = "Your Delete is Complete Successfully "
            return redirect(reverse('Event_List'))


@login_required(login_url='login')
def edit_country_list(request):
    if request.method == "POST":
        if 'Edit_COUNTRY' in request.POST:
            if request.POST.get('Edit_COUNTRY') == "UPDATE":
                COUNTRY_LIST.objects.filter(ID=request.POST.get('id')).update(
                    COUNTRY_NAME=request.POST.get('country_name'),
                )
                request.session['New_Client_Req'] = "Your Update is Complete Successfully "
            else:
                COUNTRY_LIST.objects.get(ID=request.POST.get('id')).delete()
                request.session['New_Client_Req'] = "Your Delete is Complete Successfully "
        if 'Edit_STATE' in request.POST:
            if request.POST.get('Edit_STATE') == "UPDATE":
                STATE_LIST.objects.filter(STATE_ID=request.POST.get('id')).update(
                    STATE_NAME=request.POST.get('state_name'),
                    COUNTRY_NAME=request.POST.get('country_name'),
                )
                request.session['New_Client_Req'] = "Your Update is Complete Successfully "
            else:
                STATE_LIST.objects.get(STATE_ID=request.POST.get('id')).delete()
                request.session['New_Client_Req'] = "Your Delete is Complete Successfully "
        if 'Edit_CITY' in request.POST:
            if request.POST.get('Edit_CITY') == "UPDATE":
                CITY_LIST.objects.filter(CITY_ID=request.POST.get('id')).update(
                    CITY_NAME=request.POST.get('city_name'),
                    STATE_NAME=request.POST.get('state_name'),
                    COUNTRY_NAME=request.POST.get('country_name'),
                )
                request.session['New_Client_Req'] = "Your Update is Complete Successfully "
            else:
                CITY_LIST.objects.get(CITY_ID=request.POST.get('id')).delete()
                request.session['New_Client_Req'] = "Your Delete is Complete Successfully "
        return redirect(reverse('Country_List'))


@login_required(login_url='login')
def delete_employees(request):
    if request.method == "POST":
        some_var = request.POST.getlist('checks')
        print(some_var)
        for code in some_var:
            emp_code = code
            EMP_POLICE_VERFICATION.objects.get(EMP_CODE=emp_code).delete()
            salary_details.objects.get(EMP_CODE=emp_code).delete()
            EMP_BANK_DETAILS.objects.get(EMP_CODE=emp_code).delete()
            EMP_COMMUNICATION_DETAILS.objects.get(EMP_CODE=emp_code).delete()
            EMP_PERSONAL_DETAILS.objects.get(EMP_CODE=emp_code).delete()
            EMP_COMPANY_DETAILS.objects.get(EMP_CODE=emp_code).delete()
            new_emp_reg.objects.get(EMP_CODE=emp_code).delete()

        request.session['UPDATE_EMP_DETAILS'] = "SUCCESSFULLY DELETED : " + str(some_var)
        return redirect(reverse('Employees_Management'))


@login_required(login_url='login')
def edit_employees(request):
    if request.method == "POST":
        new_emp_reg.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(
            EMP_NAME=request.POST.get('employee_name'),
            DOB=request.POST.get('dob'),
            GENDER=request.POST.get('gender'),
            SALUTATION=request.POST.get('salutation'),
            MARITAL_STATUS=request.POST.get('marital_status'),
            MOBILE_NO=request.POST.get('contact_no'),
            AGE=request.POST.get('age'),
            EXPERIANCE=request.POST.get('experiance'),
        )
        EMP_COMPANY_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(
            COUNTRY=request.POST.get('country'),
            STATE=request.POST.get('company_state'),
            DISTRICT=request.POST.get('company_district'),
            BRANCH=request.POST.get('branch'),
            AREA=request.POST.get('area'),
            CLIENT=request.POST.get('client'),
            UNIT=request.POST.get('unit'),
            DATE_OF_JOIN=request.POST.get('doj'),
            BIO_DATE_SUB_DATE=request.POST.get('bdsb'),
            DESIGNATION=request.POST.get('designation'),
            CATEGORY=request.POST.get('category'),
            ISSUE_DATE=request.POST.get('issue_date'),
            VAILD_DATE=request.POST.get('valid_date')
        )
        EMP_PERSONAL_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(
            WIFE_HUSBAND_NAME=request.POST.get('wife_husband'),
            FATHER_NAME=request.POST.get('father_name'),
            MOTHER_NAME=request.POST.get('mother_name'),
            HIGHEST_EDUCATION=request.POST.get('higher_edu'),
            BIRTH_PLACE=request.POST.get('birth_place'),
            PAN_NO=request.POST.get('pan_no'),
            PF_NO=request.POST.get('pf_no'),
            ESI_NO=request.POST.get('esi_no'),
            AADHAR_NO=request.POST.get('aadhar_no'),
            UAN_NO=request.POST.get('uan_no'),
            ID_CARD_NO=request.POST.get('id_card_no'),
            NATIONALITY=request.POST.get('nationality'),
            BLOOD_GROUP=request.POST.get('blood_group'),
            SHOE_SIZE=request.POST.get('shoe_size'),
            WAIST=request.POST.get('waist'),
            HEIGHT=request.POST.get('height'),
            WEIGHT=request.POST.get('weight'),
            CHEST=request.POST.get('chest'),
            T_SHIRT_SIZE=request.POST.get('t_shirt'),
            THOUSER_SIZE=request.POST.get('thouser_size')
        )
        EMP_COMMUNICATION_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(
            ADDRESS=request.POST.get('address'),
            STREET=request.POST.get('street'),
            DISTRICT=request.POST.get('district'),
            PINCODE=request.POST.get('pin_code'),
            TELEPHONE=request.POST.get('telephone'),
            MOBILE_NO=request.POST.get('mobile_no'),
            EMAIL_ID=request.POST.get('email_id'),
            DURATION=request.POST.get('duration'),
            STATE=request.POST.get('state'),
            PER_ADDRESS=request.POST.get('per_address'),
            PER_STREET=request.POST.get('per_street'),
            PER_DISTRICT=request.POST.get('per_district'),
            PER_PINCODE=request.POST.get('per_pin_code'),
            PER_DURATION=request.POST.get('per_duration'),
            PER_STATE=request.POST.get('per_state')

        )
        EMP_BANK_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(
            ACCOUNT_NO=request.POST.get('bank_account_no'),
            BANK_NAME=request.POST.get('bank_name'),
            IFSC_CODE=request.POST.get('ifsc_code'),
            BRANCH=request.POST.get('bank_branch'),
            PAYMENT_MODE=request.POST.get('payment_mode'),
            PASSBOOK_NAME=request.POST.get('passbook_name'),
            JOIN_ACC_NO=request.POST.get('join_acc_no'),
            JOIN_ACC_NAME=request.POST.get('join_acc_bank_name'),
            JOIN_ACC_BRANCH_NAME=request.POST.get('join_acc_name'),
            JOIN_ACC_BANK_NAME=request.POST.get('join_acc_br_name')

        )
        EMP_POLICE_VERFICATION.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(

            VERFICATION_NO=request.POST.get('verification_no'),
            VERFICATION_DATE=request.POST.get('verification_date'),
            CRIMINOLOGY=request.POST.get('criminology'),
            PV_SEND_DATE=request.POST.get('pv_send_date'),
            PV_RETURN_DATE=request.POST.get('pv_return_date'),
            NAME_OF_POLICE_THANA=request.POST.get('name_of_police_thana'),
            IDENTITY_SIGN=request.POST.get('identity_sign'),
            PV_VALID_UPTO=request.POST.get('pv_valid_date'),
            REMARK_BY_THANA=request.POST.get('remark_by_thana'),

        )
        request.session['UPDATE_EMP_DETAILS'] = "SUCCESSFULLY UPDATED : " + str(request.POST.get(
            'emp_hidden_code'))

        return redirect(reverse('Employees_Management'))
    else:
        emp_code = request.GET.get('emp_code')
        if emp_code is not None:
            newlist = []
            client = CLIENT_DETAILS.objects.all()
            for i in range(len(client)):
                variable = client[i].CLIENT
                print(variable)
                if variable not in newlist:
                    newlist.append(variable)
            print(newlist)
            designation_list = DESIGNATION_LIST.objects.filter(STATUS="Published")
            bank_list = BANK_LIST.objects.all()
            data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'EMP_BANK').filter(
                EMP_CODE=emp_code)
            value = {
                'client': newlist,
                'designation_list': designation_list,
                'bank_list': bank_list,
                'data': data,
                'emp_code': emp_code,
            }
            return render(request, 'edit_employees_details.html', value)
        else:
            return redirect(reverse('Employees_Management'))


@login_required(login_url='login')
def Filter_Employees(request):
    if request.method == "POST":
        client_list = []
        country_list = []
        filter_client = request.POST.get('client_name')
        client = CLIENT_DETAILS.objects.all()
        form_a_filter = ""
        for i in range(len(client)):
            variable = client[i].CLIENT
            print(variable, "variable")
            if variable not in client_list:
                client_list.append(variable)
        filter_value = "yes"
        result_set = []
        filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=filter_client)
        for client_details in filter_client_list:
            result_set.append(client_details)

        for i in range(len(result_set)):
            country = result_set[i].COUNTRY_NAME
            if country not in country_list:
                country_list.append(country)
        if request.POST.get('submit') == "Country":
            form_a_filter = "Country" + "~" + request.POST.get('client_name') + "~" + request.POST.get('country_name')
            country_name = request.POST.get('country_name')
            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name)
        elif request.POST.get('submit') == "State":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            form_a_filter = "State" + "~" + request.POST.get('client_name') + "~" + country_name + "~" + state_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name)
        elif request.POST.get('submit') == "District":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            form_a_filter = "District" + "~" + request.POST.get(
                'client_name') + "~" + country_name + "~" + state_name + "~" + district_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name)
        elif request.POST.get('submit') == "Branch":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            branch_name = request.POST.get('branch_name')
            form_a_filter = "Branch" + "~" + request.POST.get(
                'client_name') + "~" + country_name + "~" + state_name + "~" + district_name + "~" + branch_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name,
                                                                                   EMP_COMPANY__BRANCH=branch_name)
        elif request.POST.get('submit') == "Area":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            branch_name = request.POST.get('branch_name')
            area_name = request.POST.get('area_name')
            form_a_filter = "Branch" + "~" + request.POST.get(
                'client_name') + "~" + country_name + "~" + state_name + "~" + district_name + "~" + branch_name + "~" + area_name

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name,
                                                                                   EMP_COMPANY__BRANCH=branch_name,
                                                                                   EMP_COMPANY__AREA=area_name)
        elif request.POST.get('submit') == "Unit":
            country_name = request.POST.get('country_name')
            state_name = request.POST.get('state_name')
            district_name = request.POST.get('district_name')
            branch_name = request.POST.get('branch_name')
            area_name = request.POST.get('area_name')
            unit = request.POST.get('unit_name')
            form_a_filter = "Unit" + "~" + request.POST.get(
                'client_name') + "~" + country_name + "~" + state_name + "~" + district_name + "~" + branch_name + "~" + area_name + "~" + unit

            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client,
                                                                                   EMP_COMPANY__COUNTRY=country_name,
                                                                                   EMP_COMPANY__STATE=state_name,
                                                                                   EMP_COMPANY__DISTRICT=district_name,
                                                                                   EMP_COMPANY__BRANCH=branch_name,
                                                                                   EMP_COMPANY__AREA=area_name,
                                                                                   EMP_COMPANY__UNIT=unit)
        value = {
            'data': data,
            'client': client_list,
            'error_message': data,
            'country_list': country_list,
            'filter_value': filter_value,
            'dummy_value': filter_client,
            'form_a_filter': form_a_filter,
        }
        return render(request, 'emp_whole_details.html', value)
    else:
        if request.GET.get('client') is None:
            return redirect(reverse('Form_A'))
        else:
            get_value = request.GET.get('client').split('~')
            client_list = []
            country_list = []
            filter_client = get_value[1]
            client = CLIENT_DETAILS.objects.all()
            form_a_filter = ""
            for i in range(len(client)):
                variable = client[i].CLIENT
                print(variable, "variable")
                if variable not in client_list:
                    client_list.append(variable)
            filter_value = "yes"
            result_set = []
            filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=filter_client)
            for client_details in filter_client_list:
                result_set.append(client_details)

            for i in range(len(result_set)):
                country = result_set[i].COUNTRY_NAME
                if country not in country_list:
                    country_list.append(country)
            if get_value[0] == "Country":
                form_a_filter = "Country" + "~" + get_value[1] + "~" + get_value[2]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2])
            elif get_value[0] == "State":
                form_a_filter = "State" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3])
            elif get_value[0] == "District":
                form_a_filter = "District" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + \
                                get_value[4]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3],
                    EMP_COMPANY__DISTRICT=get_value[4])
            elif get_value[0] == "Branch":
                form_a_filter = "Branch" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + \
                                get_value[4] + "~" + get_value[5]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3],
                    EMP_COMPANY__DISTRICT=get_value[4],
                    EMP_COMPANY__BRANCH=get_value[5])
            elif get_value[0] == "Area":
                form_a_filter = "Area" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + get_value[
                    4] + "~" + get_value[5] + "~" + get_value[6]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3],
                    EMP_COMPANY__DISTRICT=get_value[4],
                    EMP_COMPANY__BRANCH=get_value[5],
                    EMP_COMPANY__AREA=get_value[6])
            elif get_value[0] == "Unit":
                form_a_filter = "Unit" + "~" + get_value[1] + "~" + get_value[2] + "~" + get_value[3] + "~" + get_value[
                    4] + "~" + get_value[5] + "~" + get_value[6] + "~" + get_value[7]
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(
                    EMP_COMPANY__CLIENT=filter_client,
                    EMP_COMPANY__COUNTRY=get_value[2],
                    EMP_COMPANY__STATE=get_value[3],
                    EMP_COMPANY__DISTRICT=get_value[4],
                    EMP_COMPANY__BRANCH=get_value[5],
                    EMP_COMPANY__AREA=get_value[6],
                    EMP_COMPANY__UNIT=get_value[7])
            value = {
                'data': data,
                'client': client_list,
                'error_message': data,
                'country_list': country_list,
                'filter_value': filter_value,
                'dummy_value': filter_client,
                'form_a_filter': form_a_filter,
            }
            return render(request, 'emp_whole_details.html', value)


@login_required(login_url='login')
def employees_management(request):
    if request.method == "POST":
        client_list = []
        country_list = []
        client = CLIENT_DETAILS.objects.all()
        for i in range(len(client)):
            variable = client[i].CLIENT
            print(variable, "variable")
            if variable not in client_list:
                client_list.append(variable)
        filter_client = request.POST.get('client')
        filter_value = "yes"
        result_set = []
        filter_client_list = CLIENT_DETAILS.objects.filter(CLIENT=filter_client)
        for client_details in filter_client_list:
            result_set.append(client_details)

        for i in range(len(result_set)):
            country = result_set[i].COUNTRY_NAME
            if country not in country_list:
                country_list.append(country)
        form = request.POST
        data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                             'NEW_EMP').filter(EMP_COMPANY__CLIENT=filter_client)
        if not data:
            filter_value = "no"
        value = {
            'data': data,
            'client': client_list,
            'error_message': data,
            'country_list': country_list,
            'filter_value': filter_value,
            'dummy_value': filter_client,
        }
        return render(request, 'emp_whole_details.html', value)

    else:
        if request.GET.get('client') is None:
            newlist = []
            client = CLIENT_DETAILS.objects.all()
            for i in range(len(client)):
                variable = client[i].CLIENT
                print(variable)
                if variable not in newlist:
                    newlist.append(variable)
            form = request.POST
            if 'UPDATE_EMP_DETAILS' not in request.session:
                stu = {
                    'client': newlist,
                }
            else:
                update_messages = request.session['UPDATE_EMP_DETAILS']
                del request.session["UPDATE_EMP_DETAILS"]

                request.session.modified = True

                stu = {
                    'client': newlist,
                    'update_messages': update_messages,
                }
        else:
            newlist = []
            country_list = []
            client = CLIENT_DETAILS.objects.all()
            for i in range(len(client)):
                variable = client[i].CLIENT
                print(variable)
                if variable not in newlist:
                    newlist.append(variable)
            filter_value = "yes"
            client = request.GET.get('client')
            result_set = []
            filter_client = CLIENT_DETAILS.objects.filter(CLIENT=client)
            for country in filter_client:
                result_set.append(country.COUNTRY_NAME)

            for i in range(len(result_set)):
                country_list = [result_set[i]]
                for e in result_set:
                    if e not in country_list:
                        country_list.append(e)
            print(newlist)
            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=client)
            stu = {
                'data': data,
                'client': newlist,
                'error_message': data,
                'country_list': country_list,
                'filter_value': filter_value,
                'dummy_value': client,
            }
    return render(request, 'emp_whole_details.html', stu)


@login_required(login_url='login')
def edit_client_details(request):
    if request.method == "POST":
        if request.POST.get('Edit_CLIENT') == "UPDATE":
            CLIENT_DETAILS.objects.filter(ID=request.POST.get('id')).update(
                CLIENT=request.POST.get('client_name'),
                COUNTRY_NAME=request.POST.get('country_name'),
                STATE_NAME=request.POST.get('state_name'),
                DISTRICT_NAME=request.POST.get('district_name'),
                BRANCH_NAME=request.POST.get('branch_name'),
                AREA_NAME=request.POST.get('area_name'),
                UNIT=request.POST.get('unit'),
                E_MAIL=request.POST.get('client_email'),
                WEB=request.POST.get('client_ph'),
                CONTACT_NO=request.POST.get('client_web'),
                ADDRESS=request.POST.get('address'),
            )
            request.session['New_Client_Req'] = "Your Update is Complete Successfully "
        else:
            CLIENT_DETAILS.objects.get(ID=request.POST.get('id')).delete()
            request.session['New_Client_Req'] = "Your Delete is Complete Successfully "
        return redirect(reverse('Client_Details'))


@login_required(login_url='login')
def edit_award_category(request):
    if request.method == "POST":
        if request.POST.get('Edit') == "UPDATE":
            AWARD_CATEGORY_LIST.objects.filter(ID=request.POST.get('id')).update(
                AWARD_CATEGORY=request.POST.get('award_name'),
                STATUS=request.POST.get('status'),
            )
            request.session['New_Client_Req'] = "Your Update is Complete Successfully "
            return redirect(reverse('Award_Category_List'))
        else:
            AWARD_CATEGORY_LIST.objects.get(ID=request.POST.get('id')).delete()
            request.session['New_Client_Req'] = "Your Delete is Complete Successfully "
            return redirect(reverse('Award_Category_List'))


def img_doc_db_url(value, emp_code):
    emp_per = EMP_PERSONAL_DETAILS.objects.get(EMP_CODE=emp_code)
    if value == "img_get":
        return emp_per.PROFILE_URL
    elif value == "doc_get":
        return emp_per.DOCUMENT_URL
    else:
        return emp_per.PROFILE_URL, emp_per.DOCUMENT_URL


def find_admin(admin_name, admin_id):
    return_admin_name = ""
    try:
        check_admin = Admin_Table.objects.get(ADMIN_NAME=admin_name, ADMIN_ID=admin_id)
        return_admin_name = check_admin.ADMIN_NAME
    except Admin_Table.DoesNotExist:
        check_admin = None
        return_admin_name = "NONE"

    return return_admin_name


def find_emp_code(emp_name):
    emp_db_code = ""
    try:
        emp_code = new_emp_reg.objects.get(EMP_NAME=emp_name)
        emp_db_code = emp_code.EMP_CODE
    except new_emp_reg.DoesNotExist:
        emp_code = None
        emp_db_code = emp_code

    return emp_db_code


def find_emp_name(emp_code):
    emp_db_code = ""
    try:
        emp_code = new_emp_reg.objects.get(EMP_CODE=emp_code)
        emp_db_code = emp_code.EMP_NAME
    except new_emp_reg.DoesNotExist:
        emp_code = None
        emp_db_code = emp_code

    return emp_db_code


def img_upload(update_url, set_value, emp_code):
    url_value = update_url.name.split(".")
    format_type = url_value[1]

    if set_value == "image_upload":
        if os.path.exists("templates/media/" + emp_code + "/" + emp_code + "_PRO." + format_type):
            os.remove("templates/media/" + emp_code + "/" + emp_code + "_PRO." + format_type)
            fs = FileSystemStorage("templates/media/" + emp_code)
            fs.save(emp_code + "_PRO." + format_type, update_url)
            update_url = "/media/" + emp_code + "/" + emp_code + "_PRO." + format_type
        else:
            fs = FileSystemStorage("templates/media/" + emp_code)
            fs.save(emp_code + "_PRO." + format_type, update_url)
            update_url = "/media/" + emp_code + "/" + emp_code + "_PRO." + format_type

    else:
        if os.path.exists("templates/media/" + emp_code + "/" + emp_code + "_DOC." + format_type):
            os.remove("templates/media/" + emp_code + "/" + emp_code + "_DOC." + format_type)
            fs = FileSystemStorage("templates/media/" + emp_code)
            fs.save(emp_code + "_DOC." + format_type, update_url)
            update_url = "/media/" + emp_code + "/" + emp_code + "_DOC." + format_type
        else:
            fs = FileSystemStorage("templates/media/" + emp_code)
            fs.save(emp_code + "_DOC." + format_type, update_url)
            update_url = "/media/" + emp_code + "/" + emp_code + "_DOC." + format_type
    return update_url


def file_upload(update_url, emp_code):
    url_value = update_url.name.split(".")
    format_type = url_value[1]
    file_name = url_value[0]
    if os.path.exists("templates/media/" + emp_code + "/" + file_name + "." + format_type):
        os.remove("templates/media/" + emp_code + "/" + file_name + "." + format_type)
        fs = FileSystemStorage("templates/media/" + emp_code)
        fs.save(file_name + "." + format_type, update_url)
        update_url = "/media/" + emp_code + "/" + file_name + "." + format_type
    else:
        fs = FileSystemStorage("templates/media/" + emp_code)
        fs.save(file_name + "." + format_type, update_url)
        update_url = "/media/" + emp_code + "/" + file_name + "." + format_type
    return update_url


def file_delete(file, folder_name):
    url_value = file.split(".")
    format_type = url_value[1]
    file_name = url_value[0]
    os.remove("templates/media/" + folder_name + "/" + file_name + "." + format_type)


@login_required(login_url='login')
def edit_employee_add_edit(request):
    if request.method == "POST":
        if request.POST.get("GetData") == "GetData":
            if request.POST.get('search_type') == "emp_no":
                emp_code = request.POST.get('emp_code')
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(EMP_CODE=emp_code)
                return render(request, 'Employee_address_edit.html', {'data': data, 'error_message': data})
            else:
                emp_code = find_emp_code(request.POST.get('emp_code'))
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(EMP_CODE=emp_code)
                return render(request, 'Employee_address_edit.html', {'data': data, 'error_message': data})
        else:
            if request.POST.get("GetData") == "UPDATE":
                if request.POST.get('permanet_address') == "on":
                    PER_ADDRESS = request.POST.get('address')
                    PER_STREET = request.POST.get('street')
                    PER_DISTRICT = request.POST.get('district')
                    PER_PINCODE = request.POST.get('pin_code')
                    PER_DURATION = request.POST.get('duration')
                    PER_STATE = request.POST.get('state')
                else:
                    PER_ADDRESS = request.POST.get('per_address')
                    PER_STREET = request.POST.get('per_street')
                    PER_DISTRICT = request.POST.get('per_district')
                    PER_PINCODE = request.POST.get('per_pin_code')
                    PER_DURATION = request.POST.get('per_duration')
                    PER_STATE = request.POST.get('per_state')

                EMP_COMMUNICATION_DETAILS.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(

                    ADDRESS=request.POST.get('address'),
                    STREET=request.POST.get('street'),
                    DISTRICT=request.POST.get('district'),
                    PINCODE=request.POST.get('pin_code'),
                    TELEPHONE=request.POST.get('telephone'),
                    MOBILE_NO=request.POST.get('mobile_no'),
                    EMAIL_ID=request.POST.get('email_id'),
                    DURATION=request.POST.get('duration'),
                    STATE=request.POST.get('state'),
                    PER_ADDRESS=PER_ADDRESS,
                    PER_STREET=PER_STREET,
                    PER_DISTRICT=PER_DISTRICT,
                    PER_PINCODE=PER_PINCODE,
                    PER_DURATION=PER_DURATION,
                    PER_STATE=PER_STATE
                )
                request.session['UPDATE_EMP_ADDRESS_DETAILS'] = "SUCCESSFULLY UPDATED : " + request.POST.get(
                    'emp_hidden_code')
                return redirect(reverse('Employee_Address'))  # We redirect to the same view

    else:
        if 'UPDATE_EMP_ADDRESS_DETAILS' not in request.session:
            return render(request, 'Employee_address_edit.html')
        else:
            update_messages = request.session['UPDATE_EMP_ADDRESS_DETAILS']
            del request.session["UPDATE_EMP_ADDRESS_DETAILS"]

            request.session.modified = True

            return render(request, 'Employee_address_edit.html',
                          {'update_messages': update_messages})


@login_required(login_url='login')
def edit_customer(request):
    if request.method == "POST":
        New_Customer_Reg.objects.filter(CLIENT_CODE=request.POST.get('client_hidden_code')).update(

            CLIENT_NAME=request.POST.get('client_name'),
            EMAIL=request.POST.get('client_email'),
            DOB=request.POST.get('doj'),
            CONTACT_NO=request.POST.get('client_ph'),
            WEB=request.POST.get('web'),
            GENTER=request.POST.get('gender'),
            EMERGENCY_CONTACT_NO=request.POST.get('emg_ph'),
            ADDRESS=request.POST.get('address'),
            CLIENT_TYPE=request.POST.get('client_type'),
        )
        messages = request.POST.get('client_name') + " YOUR DATA IS UPDATED "
        emp_code = New_Customer_Reg.objects.all()
        return redirect(reverse('Manage_Customer'), {'data': emp_code, 'message': messages})
    else:
        emp_code = request.GET.get('secure')
        if emp_code is not None:
            print(emp_code)
            emp_code = New_Customer_Reg.objects.get(CLIENT_NAME=emp_code)
            emp_db_code = emp_code.CLIENT_NAME
            em_mon_report = []
            last_id = New_Customer_Reg.objects.latest('ID')
            print(request.GET.get('secure'))
            print(last_id, "gyuguy")

            class details_class:
                CLIENT_NAME = emp_code.CLIENT_NAME
                EMAIL = emp_code.EMAIL
                DOB = emp_code.DOB
                CONTACT_NO = emp_code.CONTACT_NO
                WEB = emp_code.WEB
                EMERGENCY_CONTACT_NO = emp_code.EMERGENCY_CONTACT_NO
                ADDRESS = emp_code.ADDRESS
                CLIENT_TYPE = emp_code.CLIENT_TYPE

            em_mon_report.append(details_class)
            for detailss in em_mon_report:
                print(detailss.CLIENT_NAME)
            return render(request, 'edit_customer.html', {'data': em_mon_report, 'client_id': emp_code})
        else:
            print(emp_code)
            return render(request, 'edit_customer.html')


@login_required(login_url='login')
def edit_employee_po_ver_edit(request):
    if request.method == "POST":
        if request.POST.get("GetData") == "GetData":
            if request.POST.get('search_type') == "emp_no":
                emp_code = request.POST.get('emp_code')
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(EMP_CODE=emp_code)
                return render(request, 'Employee_police_verfication.html', {'data': data, 'error_message': data})
            else:
                emp_code = find_emp_code(request.POST.get('emp_code'))
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                     'NEW_EMP').filter(EMP_CODE=emp_code)
                return render(request, 'Employee_police_verfication.html', {'data': data, 'error_message': data})
        else:
            if request.POST.get("GetData") == "UPDATE":
                EMP_POLICE_VERFICATION.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(

                    VERFICATION_NO=request.POST.get('verification_no'),
                    VERFICATION_DATE=request.POST.get('verification_date'),
                    CRIMINOLOGY=request.POST.get('criminology'),
                    PV_SEND_DATE=request.POST.get('pv_send_date'),
                    PV_RETURN_DATE=request.POST.get('pv_return_date'),
                    NAME_OF_POLICE_THANA=request.POST.get('name_of_police_thana'),
                    IDENTITY_SIGN=request.POST.get('identity_sign'),
                    PV_VALID_UPTO=request.POST.get('pv_valid_date'),
                    REMARK_BY_THANA=request.POST.get('remark_by_thana'),

                )
                request.session['UPDATE_EMP_VERIFICATION_DETAILS'] = "SUCCESSFULLY UPDATED : " + request.POST.get(
                    'emp_hidden_code')
                return redirect(reverse('Employee_Police_Verification'))
    else:
        if 'UPDATE_EMP_VERIFICATION_DETAILS' not in request.session:
            return render(request, 'Employee_police_verfication.html')
        else:
            update_messages = request.session['UPDATE_EMP_VERIFICATION_DETAILS']
            del request.session["UPDATE_EMP_VERIFICATION_DETAILS"]

            request.session.modified = True

            return render(request, 'Employee_police_verfication.html', {'update_messages': update_messages})


@login_required(login_url='login')
def upload_file_local(request):
    if request.method == "POST":
        aadhar_no = request.POST.get('vv', '')

        upload_file = request.FILES['docfile']

        if upload_file:
            ext = x = upload_file.name.split(".")

            file_format_type = ext[1]
            fs = FileSystemStorage()
            fs.save("EMP_PROFILE." + file_format_type, upload_file)
        else:
            messages.info(request, 'Upload File Missing')

    return render(request, 'sample_upload.html')


def person_create_view(request):
    countries = Country.objects.all()
    return render(request, 'sample.html', {'countries': countries})


def getCountry(request):
    if request.method == 'GET' and request.is_ajax():

        # country_name = request.POST['country_name']
        # country_name = request.GET['cnt']
        client = request.GET.get('client', None)
        result_set = []
        all_cities = []
        answer = str(client[1:-1])
        print(answer)

        selected_country = CLIENT_DETAILS.objects.filter(CLIENT=answer)

        for country in selected_country:
            result_set.append({'name': country.COUNTRY_NAME})

        for i in range(len(result_set)):
            newlist = [result_set[i]]
            for e in result_set:
                if e not in newlist:
                    newlist.append(e)

        return HttpResponse(simplejson.dumps(newlist), content_type='application/json')
        # return JsonResponse(result_set,status = 200)

    else:
        return redirect('/')


def getState(request):
    if request.method == 'GET' and request.is_ajax():

        # country_name = request.POST['country_name']
        # country_name = request.GET['cnt']
        country_name = request.GET.get('country_name', None)
        client_name = request.GET.get('client_name', None)
        result_set = []
        newlist = []
        answer = str(country_name)
        print(answer)
        print(client_name, "clientname")

        selected_state = CLIENT_DETAILS.objects.filter(CLIENT=str(client_name), COUNTRY_NAME=answer)
        print(selected_state)
        for state in selected_state:
            print(state.STATE_NAME)
            result_set.append({'name': state.STATE_NAME})

        for i in range(len(result_set)):
            newlist = [result_set[i]]
            for e in result_set:
                if e not in newlist:
                    newlist.append(e)
        print(newlist)
        return HttpResponse(simplejson.dumps(newlist), content_type='application/json')
        # return JsonResponse(result_set,status = 200)

    else:
        return redirect('/')


def getState1(request):
    if request.method == 'GET' and request.is_ajax():

        # country_name = request.POST['country_name']
        # country_name = request.GET['cnt']
        country_name = request.GET.get('country_name', None)
        client_name = request.GET.get('client_name', None)
        result_set = []
        newlist = []
        answer = str(country_name[1:-1])
        print(answer)

        selected_state = CLIENT_DETAILS.objects.filter(CLIENT=str(client_name), COUNTRY_NAME=answer)
        print(selected_state)
        for state in selected_state:
            print(state.STATE_NAME)
            result_set.append({'name': state.STATE_NAME})

        for i in range(len(result_set)):
            newlist = [result_set[i]]
            for e in result_set:
                if e not in newlist:
                    newlist.append(e)
        print(newlist)
        return HttpResponse(simplejson.dumps(newlist), content_type='application/json')
        # return JsonResponse(result_set,status = 200)

    else:
        return redirect('/')


def getCity(request):
    if request.method == 'GET' and request.is_ajax():
        district_name = request.GET.get('district_name', None)
        client_name = request.GET.get('client_name', None)

        result_set = []
        all_roads = []

        # answer = str(city_name[1:-1])
        answer = str(district_name)

        selected_city = CLIENT_DETAILS.objects.filter(CLIENT=str(client_name), STATE_NAME=answer)

        for city in selected_city:
            print(city.DISTRICT_NAME)
            result_set.append({'name': city.DISTRICT_NAME})

        for i in range(len(result_set)):
            newlist = [result_set[i]]
            for e in result_set:
                if e not in newlist:
                    newlist.append(e)

        return HttpResponse(simplejson.dumps(newlist), content_type='application/json')
        # return JsonResponse(result_set,status = 200)

    else:
        return redirect('/')


def getBranch(request):
    if request.method == 'GET' and request.is_ajax():
        branch_name = request.GET.get('branch_name', None)
        client_name = request.GET.get('client_name', None)

        result_set = []
        all_roads = []

        # answer = str(city_name[1:-1])
        answer = str(branch_name)
        print(answer)

        selected_branch = CLIENT_DETAILS.objects.filter(CLIENT=str(client_name), DISTRICT_NAME=answer)

        for branch in selected_branch:
            result_set.append({'name': branch.BRANCH_NAME})

        for i in range(len(result_set)):
            newlist = [result_set[i]]
            for e in result_set:
                if e not in newlist:
                    newlist.append(e)

        return HttpResponse(simplejson.dumps(newlist), content_type='application/json')
        # return JsonResponse(result_set,status = 200)

    else:
        return redirect('/')


def getArea(request):
    if request.method == 'GET' and request.is_ajax():
        area_name = request.GET.get('area_name', None)
        client_name = request.GET.get('client_name', None)

        result_set = []
        all_roads = []

        # answer = str(city_name[1:-1])
        answer = str(area_name)
        print(answer)

        selected_area = CLIENT_DETAILS.objects.filter(CLIENT=str(client_name), BRANCH_NAME=answer)

        for area in selected_area:
            result_set.append({'name': area.AREA_NAME})

        for i in range(len(result_set)):
            newlist = [result_set[i]]
            for e in result_set:
                if e not in newlist:
                    newlist.append(e)

        return HttpResponse(simplejson.dumps(newlist), content_type='application/json')
        # return JsonResponse(result_set,status = 200)

    else:
        return redirect('/')


def getUnit(request):
    if request.method == 'GET' and request.is_ajax():
        # country_name = request.POST['country_name']
        # country_name = request.GET['cnt']
        unit = request.GET.get('unit', None)
        client_name = request.GET.get('client_name', None)
        result_set = []
        all_unit = []
        answer = str(unit)
        print(answer)
        selected_unit = CLIENT_DETAILS.objects.filter(CLIENT=str(client_name), AREA_NAME=answer)
        for unit in selected_unit:
            result_set.append({'name': unit.UNIT})

        for i in range(len(result_set)):
            newlist = [result_set[i]]
            for e in result_set:
                if e not in newlist:
                    newlist.append(e)

        return HttpResponse(simplejson.dumps(newlist), content_type='application/json')
        # return JsonResponse(result_set,status = 200)
    else:
        return redirect('/')


@login_required(login_url='login')
def employee_monthly_attendance(request):
    countries = Country.objects.all()
    client = Client.objects.all()
    if request.method == "POST":
        if request.POST.get("GetData") == "GetData":
            client_value = request.POST.get("client")
            unit = request.POST.get("unit")
            try:
                data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                     'NEW_EMP').filter(EMP_COMPANY__CLIENT=client_value,
                                                                                       EMP_COMPANY__UNIT=unit)
                em_mon_report = []
                count = 0

                for details in data:
                    count += 1
                    ext = request.POST.get("date_month").split("-")
                    report = find_emp_monthly_atten(details.EMP_CODE, ext[1], ext[0])

                    class details_class:
                        ID = count
                        UNIT_NAME = details.EMP_COMPANY.UNIT
                        EMP_CODE = details.EMP_CODE
                        EMP_NAME = details.NEW_EMP.EMP_NAME
                        FATHER_NAME = details.EMP_PER.FATHER_NAME
                        ACC_NO = details.EMP_BANK.ACCOUNT_NO + " / " + details.EMP_BANK.BANK_NAME
                        DESIGNATION = details.EMP_COMPANY.DESIGNATION
                        DAYS_PRESENT = report.DAYS_PRESENT
                        OVERTIME = report.OVERTIME_HRS
                        SHIFT_ALLOWANCES_HRS = report.SHIFT_ALLOWANCES_HRS
                        BASIC = report.BASIC
                        SALARY_ADVANCE = report.SALARY_ADVANCE
                        PROFESSIONAL_TAX = report.PROFESSIONAL_TAX
                        INCOME_TAX = report.INCOME_TAX
                        OTHER_DEDUCTION = report.OTHER_DEDUCTION
                        edit = details.EMP_CODE

                    em_mon_report.append(details_class)

                val_len = len(em_mon_report)
                print(val_len, "length")
                if val_len >= 1:
                    return render(request, 'Monthly_Attendance.html',
                                  {'countries': countries, 'client': client, 'form': request.POST,
                                   'em_mon_report': em_mon_report})
                else:
                    print(val_len, "length")
                    return render(request, 'Monthly_Attendance.html',
                                  {'countries': countries, 'client': client, 'form': request.POST,
                                   'error': "VALUE NOT FOUND, RESET AND SEARCH AGAIN"})

            except EMP_POLICE_VERFICATION.DoesNotExist:

                return render(request, 'Monthly_Attendance.html',
                              {'countries': countries, 'client': client, 'form': request.POST,
                               'error': "VALUE NOT FOUND"})

    return render(request, 'Monthly_Attendance.html', {'countries': countries, 'client': client, 'form': request.POST})


def find_client_details(emp_code):
    class details_class:
        CLIENT_NAME = ""
        EMAIL = ""
        DOB = ""
        CONTACT_NO = ""
        WEB = ""
        GENTER = ""
        EMERGENCY_CONTACT_NO = ""
        ADDRESS = ""
        CLIENT_TYPE = 0

    try:

        emp_details = New_Customer_Reg.objects.get(CLIENT_CODE=emp_code)
        details_class.CLIENT_NAME = emp_details.CLIENT_NAME
    except Monthly_Attendance_Table.DoesNotExist:
        print("VALUE NOT FOUNT IN DB", emp_code, year, month)

    return details_class


def find_emp_monthly_atten(emp_code, year, month):
    class details_class:
        DAYS_PRESENT = 0
        FIXED_SALARY = 0
        MONTH_SALARY = 0
        BASIC = 0
        DEARANCE_ALLOWANCES = 0
        SPECIAL_ALLOWANCES = 0
        HOUSE_RENT_ALLOWANCES = 0
        CONVEYANCE = 0
        OTHER_ALLOWANCES = 0
        OVERTIME_AMOUNT = 0
        OVERTIME_HRS = 0
        SITE_ALLOWANCES = 0
        SHIFT_ALLOWANCES_AMOUNT = 0
        SHIFT_ALLOWANCES_HRS = 0
        INCENTIVE = 0
        LEAVE_TRAVEL_ALLOWANCES = 0
        MEDICAL_ALLOWANCES = 0
        CHILD_EDUCATIONS_ALLOWANCES = 0
        ATTENDANCE_BONUS = 0
        ATTENDANCE_INCENTIVE = 0
        MONTHLY_BOUNS = 0
        MONTHLY_LEAVE_WAGES = 0
        ESIC = 0
        RELIVER_DUTY_WAGES = 0
        ARREARS_WAGES = 0
        PROVIDENT_FUND = 0
        PROFESSIONAL_TAX = 0
        LABOUR_WELFARE_FUND = 0
        INCOME_TAX = 0
        LOAN = 0
        SALARY_ADVANCE = 0
        OTHER_DEDUCTION = 0
        UNIFORM_DEDUCTION = 0
        EXTRA_BONUS = 0

    try:

        emp_details = EMP_SALARY_MAINTAINS.objects.get(EMP_CODE=emp_code, SALARY_UPDATE_DATE=month + "-" + year)
        print(emp_code, "emp code")
        details_class.FIXED_SALARY = emp_details.FIXED_SALARY
        details_class.MONTH_SALARY = emp_details.MONTH_SALARY
        details_class.BASIC = emp_details.BASIC
        details_class.DEARANCE_ALLOWANCES = emp_details.DEARANCE_ALLOWANCES
        details_class.SPECIAL_ALLOWANCES = emp_details.SPECIAL_ALLOWANCES
        details_class.HOUSE_RENT_ALLOWANCES = emp_details.HOUSE_RENT_ALLOWANCES
        details_class.CONVEYANCE = emp_details.CONVEYANCE
        details_class.OTHER_ALLOWANCES = emp_details.OTHER_ALLOWANCES
        details_class.OVERTIME_AMOUNT = emp_details.OVERTIME_AMOUNT
        details_class.SITE_ALLOWANCES = emp_details.SITE_ALLOWANCES
        details_class.SHIFT_ALLOWANCES_AMOUNT = emp_details.SHIFT_ALLOWANCES_AMOUNT
        details_class.INCENTIVE = emp_details.INCENTIVE
        details_class.LEAVE_TRAVEL_ALLOWANCES = emp_details.LEAVE_TRAVEL_ALLOWANCES
        details_class.MEDICAL_ALLOWANCES = emp_details.MEDICAL_ALLOWANCES
        details_class.CHILD_EDUCATIONS_ALLOWANCES = emp_details.CHILD_EDUCATIONS_ALLOWANCES
        details_class.ATTENDANCE_BONUS = emp_details.ATTENDANCE_BONUS
        details_class.ATTENDANCE_INCENTIVE = emp_details.ATTENDANCE_INCENTIVE
        details_class.MONTHLY_BOUNS = emp_details.MONTHLY_BOUNS
        details_class.EXTRA_BOUNS = emp_details.EXTRA_BOUNS
        details_class.MONTHLY_LEAVE_WAGES = emp_details.MONTHLY_LEAVE_WAGES
        details_class.ESIC = emp_details.ESIC
        details_class.RELIVER_DUTY_WAGES = emp_details.RELIVER_DUTY_WAGES
        details_class.ARREARS_WAGES = emp_details.ARREARS_WAGES
        details_class.PROVIDENT_FUND = emp_details.PROVIDENT_FUND
        details_class.PROFESSIONAL_TAX = emp_details.PROFESSIONAL_TAX
        details_class.LABOUR_WELFARE_FUND = emp_details.LABOUR_WELFARE_FUND
        details_class.INCOME_TAX = emp_details.INCOME_TAX
        details_class.LOAN = emp_details.LOAN
        details_class.SALARY_ADVANCE = emp_details.SALARY_ADVANCE
        details_class.OTHER_DEDUCTION = emp_details.OTHER_DEDUCTION
        details_class.UNIFORM_DEDUCTION = emp_details.UNIFORM_DEDUCTION
        details_class.TOTAL_EARN = emp_details.TOTAL_EARN
        details_class.TOTAL_DEDUCATION = emp_details.TOTAL_DEDUCATION
        details_class.NET_PAY = emp_details.NET_PAY

        try:
            report = Monthly_Attendance_Table.objects.get(EMP_CODE=emp_code, YEAR=year, MONTH=month)
            details_class.DAYS_PRESENT = report.DAYS_PRESENT
            details_class.OVERTIME_HRS = report.OVERTIME_HRS
            details_class.SHIFT_ALLOWANCES_HRS = report.SHIFT_ALLOWANCES_HRS
        except Monthly_Attendance_Table.DoesNotExist:
            print("VALUE NOT FOUNT IN DB", emp_code, year, month)
    except EMP_SALARY_MAINTAINS.DoesNotExist:
        print("VALUE NOT FOUNT IN DB", emp_code, year, month)

    return details_class


@login_required(login_url='login')
def employee_monthly_attendance_edit(request):
    if request.method == "GET":
        ext = request.GET.get("year").split("-")
        report = find_emp_monthly_atten(request.GET.get("secure"), ext[1], ext[0])
        report_array = []
        report_array.append(report)
        print(report_array)
        return render(request, 'Monthly_Attendance_Edit.html', {'data': report_array, 'url': request.GET})

    elif request.method == "POST":
        if request.POST.get("GetData") == "UPDATE":
            ext = request.POST.get("year").split("-")
            try:
                report = Monthly_Attendance_Table.objects.get(EMP_CODE=request.GET.get("secure"), YEAR=ext[1],
                                                              MONTH=ext[0])
                Monthly_Attendance_Table.objects.filter(EMP_CODE=request.POST.get('secure'), YEAR=ext[1],
                                                        MONTH=ext[0]).update(
                    DAYS_PRESENT=request.POST.get('day_per'),
                    OVERTIME_HRS=request.POST.get('ot_hrs'),
                    SHIFT_ALLOWANCES_HRS=request.POST.get('e_sf_hrs'),
                )
            except Monthly_Attendance_Table.DoesNotExist:

                insert = Monthly_Attendance_Table(

                    EMP_CODE=request.GET.get("secure"),
                    DAYS_PRESENT=request.POST.get('day_per'),
                    OVERTIME_HRS=request.POST.get('ot_hrs'),
                    SHIFT_ALLOWANCES_HRS=request.POST.get('e_sf_hrs'),
                    YEAR=ext[1],
                    MONTH=ext[0],
                )
                insert.save()

            report = find_emp_monthly_atten(request.GET.get("secure"), ext[1], ext[0])
            report_array = []
            report_array.append(report)
            return render(request, 'Monthly_Attendance_Edit.html', {'data': report_array, 'url': request.POST})
    else:
        return redirect('/')


def salary_slip(request):
    client = Client.objects.all()
    if request.method == "POST":
        if request.POST.get("GetData") == "GetData":

            client_value = request.POST.get("client")
            print(client_value, "client")
            unit = request.POST.get("unit")
            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=client_value,
                                                                                   EMP_COMPANY__UNIT=unit)
            em_mon_report = []
            count = 0
            print(data)
            for details in data:
                count += 1
                ext = request.POST.get("date_month").split("-")
                report = find_emp_monthly_atten(details.EMP_CODE, ext[1], ext[0])
                print("DAYS_PRESENT-->", unit)
                if report.DAYS_PRESENT >= 1:
                    class details_class:
                        id = count
                        token_no = "VAES102" + str(id)
                        emp_name = details.NEW_EMP.EMP_NAME
                        emp_code = details.EMP_CODE
                        father_name = details.EMP_PER.FATHER_NAME
                        print = details.EMP_CODE + "~" + ext[1] + "~" + ext[0] + "~" + details.EMP_COMPANY.DESIGNATION

                    em_mon_report.append(details_class)

            val_len = len(em_mon_report)
            if val_len >= 1:
                return render(request, 'Salary_Slip.html',
                              {'client': client, 'form': request.POST,
                               'em_mon_report': em_mon_report})
            else:
                return render(request, 'Salary_Slip.html',
                              {'client': client, 'form': request.POST,
                               'error': "VALUE NOT FOUND, RESET AND SEARCH AGAIN"})
            # return render(request, 'Salary_Slip.html', {'client': client})
    return render(request, 'Salary_Slip.html', {'client': client})


def salary_slip_invoice(request):
    if request.method == "GET":
        ext = request.GET.get("secure").split("~")
        print(ext[1])
        emp_name = find_emp_name(ext[0])
        data = EMP_POLICE_VERFICATION.objects.select_related('NEW_EMP', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',

                                                             'EMP_BANK').get(EMP_CODE=ext[0])
        client_name = data.EMP_COMPANY.CLIENT
        county_name = data.EMP_COMPANY.COUNTRY
        state_name = data.EMP_COMPANY.STATE
        district_name = data.EMP_COMPANY.DISTRICT
        branch_name = data.EMP_COMPANY.BRANCH
        area_name = data.EMP_COMPANY.AREA
        unit = data.EMP_COMPANY.UNIT
        emp_code = data.NEW_EMP.EMP_CODE
        uan_no = data.EMP_PER.UAN_NO
        esic_no = data.EMP_PER.ESI_NO
        doj = data.EMP_COMPANY.DATE_OF_JOIN
        bank_name = data.EMP_BANK.BANK_NAME
        acc_no = data.EMP_BANK.ACCOUNT_NO
        ifsc_code = data.EMP_BANK.IFSC_CODE

        address = CLIENT_DETAILS.objects.get(CLIENT=client_name,
                                             COUNTRY_NAME=county_name,
                                             STATE_NAME=state_name,
                                             DISTRICT_NAME=district_name,
                                             BRANCH_NAME=branch_name,
                                             AREA_NAME=area_name,
                                             UNIT=unit)
        if ext[1] == "NO UPDATED":
            print(type(ext), "if")
            report = salary_details.objects.filter(EMP_CODE=ext[0])
            report_array = []
            report_array.append(report)

            value = {
                'client': report, 'emp_name': ext[3],
                'desgin': ext[2], 'year': "UPDATED",
                'month': "NO", 'client_name': client_name,
                'emp_code': emp_code, 'address': address.ADDRESS,
                'uan_no': uan_no, 'esic_no': esic_no, 'ifsc_code': ifsc_code,
                'emp_name': emp_name, 'doj': doj, 'bank_name': bank_name, 'acc_no': acc_no,

            }

        else:
            report = find_emp_monthly_atten(ext[0], ext[1], ext[2])
            report_array = []
            report_array.append(report)
            value = {
                'client': report_array, 'emp_name': emp_name,
                'desgin': ext[3], 'year': ext[1],
                'month': ext[2], 'client_name': client_name, 'emp_code': emp_code,
                'address': address.ADDRESS, 'uan_no': uan_no, 'esic_no': esic_no,
                'doj': doj, 'bank_name': bank_name, 'acc_no': acc_no, 'ifsc_code': ifsc_code,
            }
        return render(request, 'salary_slip_invoic.html', value)


def Employee_Report(request):
    country_list = Country.objects.all()
    client = Client.objects.all()
    if request.method == "POST":
        if request.POST.get("GetData") == "GetData":
            client_value = request.POST.get("client")
            unit = request.POST.get("unit")
            COUNTRY = request.POST.get("country")
            STATE = request.POST.get("state")
            DISTRICT = request.POST.get("city")
            print(request.POST)
            data = EMP_POLICE_VERFICATION.objects.select_related('EMP_BANK', 'EMP_COMM', 'EMP_PER', 'EMP_COMPANY',
                                                                 'NEW_EMP').filter(EMP_COMPANY__CLIENT=client_value,
                                                                                   EMP_COMPANY__UNIT=unit,
                                                                                   EMP_COMPANY__COUNTRY=COUNTRY,
                                                                                   EMP_COMPANY__STATE=STATE,
                                                                                   EMP_COMPANY__DISTRICT=DISTRICT)
            em_mon_report = []
            count = 0
            for details in data:
                count += 1

                class details_class:
                    id = count
                    emp_code = details.EMP_CODE
                    emp_name = details.NEW_EMP.EMP_NAME
                    father_name = details.EMP_PER.FATHER_NAME
                    design = details.EMP_COMPANY.DESIGNATION
                    client_name = details.EMP_COMPANY.CLIENT
                    unit = details.EMP_COMPANY.UNIT
                    dob = details.NEW_EMP.DOB
                    join_date = details.NEW_EMP.REG_DATE
                    blood_grp = details.EMP_PER.BLOOD_GROUP
                    pv_date = details.PV_RETURN_DATE + "/" + details.VERFICATION_NO
                    vo_id = details.EMP_PER.AADHAR_NO
                    mobile = details.NEW_EMP.MOBILE_NO

                em_mon_report.append(details_class)

            val_len = len(em_mon_report)
            if val_len >= 1:
                return render(request, 'Report_Employee.html',
                              {'countries': country_list, 'client': client, 'em_mon_report': em_mon_report})
            else:
                return render(request, 'Report_Employee.html',
                              {'countries': country_list, 'client': client,
                               'error': "VALUE NOT FOUND, RESET AND SEARCH AGAIN"})
    return render(request, 'Report_Employee.html', {'countries': country_list, 'client': client})


def delete_all_employees(request):
    EMP_POLICE_VERFICATION.objects.all().delete()
    salary_details.objects.all().delete()
    EMP_BANK_DETAILS.objects.all().delete()
    EMP_COMMUNICATION_DETAILS.objects.all().delete()
    EMP_PERSONAL_DETAILS.objects.all().delete()
    EMP_COMPANY_DETAILS.objects.all().delete()
    new_emp_reg.objects.all().delete()


def delete_all_employees_attendance(request):
    EMP_DAILY_ATTENDANCE_UPDATED.objects.all().delete()


def Insert_Country(request):
    Country.objects.all().delete()
    State.objects.all().delete()
    City.objects.all().delete()

    contry = Country(Country_Name="INDIA")
    contry.save()

    St = State(
        State_Name="TAMILNADU",
        Country=contry
    )
    St.save()

    CY = City(
        City_Name="CHENNAI",
        Country=St
    )
    CY.save()

    CY = City(
        City_Name="MADURAI",
        Country=St
    )
    CY.save()

    CY = City(
        City_Name="KONGU NADU",
        Country=St
    )
    CY.save()

    St = State(
        State_Name="KERALA",
        Country=contry
    )
    St.save()

    CY = City(
        City_Name="KOCHI",
        Country=St
    )
    CY.save()
    contry = Country(Country_Name="USA")
    contry.save()


def Insert_CLIENT(request):
    Client.objects.all().delete()
    Unit.objects.all().delete()
    cl = Client(
        Client_Name="VALIANCE TECHONOLOGY"
    )
    cl.save()

    ut = Unit(Unit_Name="HOM,CHENNAI", Client=cl)
    ut.save()

    ut = Unit(Unit_Name="REGIONAL OFFICE,CHENNAI", Client=cl)
    ut.save()

    ut = Unit(Unit_Name="TONDIARPET,CHENNAI", Client=cl)
    ut.save()

    cl = Client(
        Client_Name="PUPA CLICK"
    )
    cl.save()

    ut = Unit(Unit_Name="HEAD OFFICE ,CHENNAI", Client=cl)
    ut.save()

    cl = Client(
        Client_Name="HCL"
    )
    cl.save()
    cl = Client(
        Client_Name="TCS"
    )
    cl.save()


@login_required(login_url='login')
def edit_employee_salary_edit(request):
    if request.method == "POST":
        if request.POST.get("GetData") == "GetData":
            if request.POST.get('search_type') == "emp_no":
                emp_code = request.POST.get('emp_code')
                try:
                    data1 = salary_details.objects.get(EMP_CODE=emp_code)
                    # data1 = salary_details.objects.filter(EMP_CODE=emp_code)
                    data = screenshots_as_list(data1)
                    print(data1.FIXED_SALARY, "---------")
                    report_array = []
                    report_array.append(data)
                    return render(request, 'Employee_salary_edit.html', {'data': report_array, 'emp_id': emp_code})
                except salary_details.DoesNotExist:
                    return render(request, 'Employee_salary_edit.html', {'error': "EMPLOYEE NOT FOUND"})
            else:
                emp_code = find_emp_code(request.POST.get('emp_code'))
                data1 = salary_details.objects.filter(EMP_CODE=emp_code)
                data = screenshots_as_list(data1)
                return render(request, 'Employee_salary_edit.html',
                              {'data': data, 'error_message': "VALUE NOT FOUND, RESET AND SEARCH AGAIN"})
        else:
            if request.POST.get("GetData") == "UPDATE":
                emp_code = request.POST.get('emp_hidden_code')
                ext = request.POST.get("date_month")
                print(request.POST.get('mon_esic'))
                if ext == "NO UPDATED":
                    salary_details.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(

                        FIXED_SALARY=request.POST.get('fix_sal'),
                        BASIC=request.POST.get('basic'),
                        DEARANCE_ALLOWANCES=request.POST.get('dea_all'),
                        SPECIAL_ALLOWANCES=request.POST.get('spa'),
                        HOUSE_RENT_ALLOWANCES=request.POST.get('hra'),
                        CONVEYANCE=request.POST.get('con'),
                        OTHER_ALLOWANCES=request.POST.get('ota'),
                        OVERTIME_AMOUNT=0,
                        SITE_ALLOWANCES=request.POST.get('sta'),
                        SHIFT_ALLOWANCES_AMOUNT=request.POST.get('e_sf_pay'),
                        INCENTIVE=request.POST.get('inc'),
                        LEAVE_TRAVEL_ALLOWANCES=0,
                        MEDICAL_ALLOWANCES=request.POST.get('med_a'),
                        CHILD_EDUCATIONS_ALLOWANCES=request.POST.get('cea'),
                        ATTENDANCE_BONUS=request.POST.get('att_bo'),
                        ATTENDANCE_INCENTIVE=request.POST.get('att_in'),
                        MONTHLY_BOUNS=0,
                        MONTHLY_LEAVE_WAGES=request.POST.get('mon_le_wa'),
                        PROVIDENT_FUND=0,
                        PENSION_AMOUNT=0,
                        ESIC=0,
                        RELIVER_DUTY_WAGES=request.POST.get('re_du_wa'),
                        ARREARS_WAGES=request.POST.get('arr_wa'),
                        PROFESSIONAL_TAX=0,
                        LABOUR_WELFARE_FUND=0,
                        INCOME_TAX=request.POST.get('income_tax'),
                        LOAN=request.POST.get('loan'),
                        SALARY_ADVANCE=request.POST.get('salary_adv'),
                        OTHER_DEDUCTION=request.POST.get('other_dec'),
                        UNIFORM_DEDUCTION=request.POST.get('uni_dec'),
                        TOTAL_EARN=0,
                        TOTAL_DEDUCATION=0,
                        NET_PAY=0,
                        SALARY_UPDATE_DATE=request.POST.get("date_month"),
                        EXTRA_BOUNS=request.POST.get('extra_bo'),
                    )
                    request.session['UPDATE_EMP_SALARY_DETAILS'] = "SUCCESSFULLY UPDATED : " + request.POST.get(
                        'emp_hidden_code')
                else:
                    ext = request.POST.get("date_month").split("-")
                    try:
                        emp_over_time = Monthly_Attendance_Table.objects.get(EMP_CODE=emp_code, MONTH=ext[0],
                                                                             YEAR=ext[1])
                        print(emp_over_time, "fagagag")
                        emp_month_data = emp_over_time.OVERTIME_HRS
                        print(emp_month_data, "overtime")
                        basic = int(request.POST.get('basic'))
                        da = int(request.POST.get('dea_all'))
                        onehr_salary = (int(request.POST.get('fix_sal')) / 30) / 8
                        oneday_salary = (int(request.POST.get('fix_sal')) / 30)
                        over_time_sal = emp_month_data * 2
                        emp_over_time_amount = onehr_salary * over_time_sal
                        month_salary = int(emp_over_time.DAYS_PRESENT) * oneday_salary

                        LEAVE_TRAVEL = basic / 12
                        PROFESSIONAL_TAX = (basic * 0.25) / 100
                        LABOUR_WELFARE_FUND = (basic * 0.10) / 100
                        PENSION_AMOUNT = (basic * 8.33) / 100
                        monthly_bonus = (basic * 8.33) / 100
                        PROVIDENTFUND = (basic * 3.67) / 100
                        total_earn = month_salary + emp_over_time_amount + LEAVE_TRAVEL + monthly_bonus \
                                     + int(request.POST.get('spa')) + int(
                            request.POST.get('con')) + int(request.POST.get('ota')) \
                                     + int(request.POST.get('sta')) + int(request.POST.get('e_sf_pay')) + int(
                            request.POST.get('inc')) \
                                     + int(request.POST.get('med_a')) + int(request.POST.get('cea')) + int(
                            request.POST.get('att_bo')) \
                                     + int(request.POST.get('att_in')) + int(request.POST.get('arr_wa')) + int(
                            request.POST.get('mon_le_wa')) + int(request.POST.get('extra_bo')) \
                                     + int(request.POST.get('re_du_wa'))
                        esic = (total_earn * 0.75) / 100
                        print(esic, "esic")

                        total_deducation = PROVIDENTFUND + esic + PENSION_AMOUNT + LABOUR_WELFARE_FUND + PROFESSIONAL_TAX \
                                           + int(request.POST.get('income_tax')) + int(request.POST.get('loan')) + int(
                            request.POST.get('salary_adv')) \
                                           + int(request.POST.get('other_dec')) + int(request.POST.get('uni_dec'))
                        net_pay = total_earn - total_deducation
                        try:
                            EMP_SALARY_MAINTAINS.objects.get(EMP_CODE=emp_code,
                                                             SALARY_UPDATE_DATE=ext[0] + "-" + ext[1])

                            EMP_SALARY_MAINTAINS.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code'),
                                                                SALARY_UPDATE_DATE=ext[0] + "-" + ext[1]).update(
                                FIXED_SALARY=request.POST.get('fix_sal'),
                                MONTH_SALARY=month_salary,
                                BASIC=basic,
                                DEARANCE_ALLOWANCES=request.POST.get('dea_all'),
                                SPECIAL_ALLOWANCES=request.POST.get('spa'),
                                HOUSE_RENT_ALLOWANCES=request.POST.get('hra'),
                                CONVEYANCE=request.POST.get('con'),
                                OTHER_ALLOWANCES=request.POST.get('ota'),
                                OVERTIME_AMOUNT="{:.2f}".format(emp_over_time_amount),
                                SITE_ALLOWANCES=request.POST.get('sta'),
                                SHIFT_ALLOWANCES_AMOUNT=request.POST.get('e_sf_pay'),
                                INCENTIVE=request.POST.get('inc'),
                                LEAVE_TRAVEL_ALLOWANCES="{:.2f}".format(LEAVE_TRAVEL),
                                MEDICAL_ALLOWANCES=request.POST.get('med_a'),
                                CHILD_EDUCATIONS_ALLOWANCES=request.POST.get('cea'),
                                ATTENDANCE_BONUS=request.POST.get('att_bo'),
                                ATTENDANCE_INCENTIVE=request.POST.get('att_in'),
                                MONTHLY_BOUNS="{:.2f}".format(monthly_bonus),
                                MONTHLY_LEAVE_WAGES=request.POST.get('mon_le_wa'),
                                PROVIDENT_FUND=PROVIDENTFUND,
                                PENSION_AMOUNT="{:.2f}".format(PENSION_AMOUNT),
                                ESIC="{:.2f}".format(esic),
                                RELIVER_DUTY_WAGES=request.POST.get('re_du_wa'),
                                ARREARS_WAGES=request.POST.get('arr_wa'),
                                PROFESSIONAL_TAX="{:.2f}".format(PROFESSIONAL_TAX),
                                LABOUR_WELFARE_FUND="{:.2f}".format(LABOUR_WELFARE_FUND),
                                INCOME_TAX=request.POST.get('income_tax'),
                                LOAN=request.POST.get('loan'),
                                SALARY_ADVANCE=request.POST.get('salary_adv'),
                                OTHER_DEDUCTION=request.POST.get('other_dec'),
                                UNIFORM_DEDUCTION=request.POST.get('uni_dec'),
                                TOTAL_EARN="{:.2f}".format(total_earn),
                                TOTAL_DEDUCATION="{:.2f}".format(total_deducation),
                                NET_PAY="{:.2f}".format(net_pay),
                                SALARY_UPDATE_DATE=request.POST.get("date_month"),
                                EXTRA_BOUNS=request.POST.get('extra_bo'),
                                DAYS_PRESENT=emp_over_time.DAYS_PRESENT,
                                OVERTIME_HRS=emp_over_time.OVERTIME_HRS,
                                SHIFT_ALLOWANCES_HRS=emp_over_time.SHIFT_ALLOWANCES_HRS,
                            )
                        except EMP_SALARY_MAINTAINS.DoesNotExist:
                            salary_maintains = EMP_SALARY_MAINTAINS(
                                EMP_CODE=request.POST.get('emp_hidden_code'),
                                FIXED_SALARY=request.POST.get('fix_sal'),
                                MONTH_SALARY=month_salary,
                                BASIC=basic,
                                DEARANCE_ALLOWANCES=request.POST.get('dea_all'),
                                SPECIAL_ALLOWANCES=request.POST.get('spa'),
                                HOUSE_RENT_ALLOWANCES=request.POST.get('hra'),
                                CONVEYANCE=request.POST.get('con'),
                                OTHER_ALLOWANCES=request.POST.get('ota'),
                                OVERTIME_AMOUNT="{:.2f}".format(emp_over_time_amount),
                                SITE_ALLOWANCES=request.POST.get('sta'),
                                SHIFT_ALLOWANCES_AMOUNT=request.POST.get('e_sf_pay'),
                                INCENTIVE=request.POST.get('inc'),
                                LEAVE_TRAVEL_ALLOWANCES="{:.2f}".format(LEAVE_TRAVEL),
                                MEDICAL_ALLOWANCES=request.POST.get('med_a'),
                                CHILD_EDUCATIONS_ALLOWANCES=request.POST.get('cea'),
                                ATTENDANCE_BONUS=request.POST.get('att_bo'),
                                ATTENDANCE_INCENTIVE=request.POST.get('att_in'),
                                MONTHLY_BOUNS="{:.2f}".format(monthly_bonus),
                                MONTHLY_LEAVE_WAGES=request.POST.get('mon_le_wa'),
                                PROVIDENT_FUND=PROVIDENTFUND,
                                ESIC="{:.2f}".format(esic),
                                PENSION_AMOUNT="{:.2f}".format(PENSION_AMOUNT),
                                RELIVER_DUTY_WAGES=request.POST.get('re_du_wa'),
                                ARREARS_WAGES=request.POST.get('arr_wa'),
                                PROFESSIONAL_TAX="{:.2f}".format(PROFESSIONAL_TAX),
                                LABOUR_WELFARE_FUND="{:.2f}".format(LABOUR_WELFARE_FUND),
                                INCOME_TAX=request.POST.get('income_tax'),
                                LOAN=request.POST.get('loan'),
                                SALARY_ADVANCE=request.POST.get('salary_adv'),
                                her_OTHER_DEDUCTION=request.POST.get('otdec'),
                                UNIFORM_DEDUCTION=request.POST.get('uni_dec'),
                                TOTAL_EARN="{:.2f}".format(total_earn),
                                TOTAL_DEDUCATION="{:.2f}".format(total_deducation),
                                NET_PAY="{:.2f}".format(net_pay),
                                SALARY_UPDATE_DATE=request.POST.get("date_month"),
                                EXTRA_BOUNS=request.POST.get('extra_bo'),
                                DAYS_PRESENT=emp_over_time.DAYS_PRESENT,
                                OVERTIME_HRS=emp_over_time.OVERTIME_HRS,
                                SHIFT_ALLOWANCES_HRS=emp_over_time.SHIFT_ALLOWANCES_HRS,
                            )
                            salary_maintains.save()

                        salary_details.objects.filter(EMP_CODE=request.POST.get('emp_hidden_code')).update(
                            FIXED_SALARY=request.POST.get('fix_sal'),
                            MONTH_SALARY=month_salary,
                            BASIC=basic,
                            DEARANCE_ALLOWANCES=request.POST.get('dea_all'),
                            SPECIAL_ALLOWANCES=request.POST.get('spa'),
                            HOUSE_RENT_ALLOWANCES=request.POST.get('hra'),
                            CONVEYANCE=request.POST.get('con'),
                            OTHER_ALLOWANCES=request.POST.get('ota'),
                            OVERTIME_AMOUNT="{:.2f}".format(emp_over_time_amount),
                            SITE_ALLOWANCES=request.POST.get('sta'),
                            SHIFT_ALLOWANCES_AMOUNT=request.POST.get('e_sf_pay'),
                            INCENTIVE=request.POST.get('inc'),
                            LEAVE_TRAVEL_ALLOWANCES="{:.2f}".format(LEAVE_TRAVEL),
                            MEDICAL_ALLOWANCES=request.POST.get('med_a'),
                            CHILD_EDUCATIONS_ALLOWANCES=request.POST.get('cea'),
                            ATTENDANCE_BONUS=request.POST.get('att_bo'),
                            ATTENDANCE_INCENTIVE=request.POST.get('att_in'),
                            MONTHLY_BOUNS="{:.2f}".format(monthly_bonus),
                            MONTHLY_LEAVE_WAGES=request.POST.get('mon_le_wa'),
                            PROVIDENT_FUND=PROVIDENTFUND,
                            ESIC="{:.2f}".format(esic),
                            PENSION_AMOUNT="{:.2f}".format(PENSION_AMOUNT),
                            RELIVER_DUTY_WAGES=request.POST.get('re_du_wa'),
                            ARREARS_WAGES=request.POST.get('arr_wa'),
                            PROFESSIONAL_TAX="{:.2f}".format(PROFESSIONAL_TAX),
                            LABOUR_WELFARE_FUND="{:.2f}".format(LABOUR_WELFARE_FUND),
                            INCOME_TAX=request.POST.get('income_tax'),
                            LOAN=request.POST.get('loan'),
                            SALARY_ADVANCE=request.POST.get('salary_adv'),
                            OTHER_DEDUCTION=request.POST.get('other_dec'),
                            UNIFORM_DEDUCTION=request.POST.get('uni_dec'),
                            TOTAL_EARN="{:.2f}".format(total_earn),
                            TOTAL_DEDUCATION="{:.2f}".format(total_deducation),
                            NET_PAY="{:.2f}".format(net_pay),
                            SALARY_UPDATE_DATE=request.POST.get("date_month"),
                            EXTRA_BOUNS=request.POST.get('extra_bo'),
                        )
                        request.session['UPDATE_EMP_SALARY_DETAILS'] = "SUCCESSFULLY UPDATED : " + request.POST.get(
                            'emp_hidden_code')
                    except Monthly_Attendance_Table.DoesNotExist:
                        request.session['UPDATE_EMP_SALARY_DETAILS'] = request.POST.get(
                            "date_month") + " MONTHLY ATTENTDANCE NOT  UPDATED : " + request.POST.get(
                            'emp_hidden_code')
                return redirect(reverse('Employee_Salary_Details'))
    else:
        if 'UPDATE_EMP_SALARY_DETAILS' not in request.session:
            emp_code = request.GET.get('secure')
            emp_data = salary_details.objects.get(EMP_CODE=emp_code)
            data = screenshots_as_list(emp_data)
            print(emp_data.FIXED_SALARY, "---------")
            report_array = []
            report_array.append(data)
            return render(request, 'Employee_salary_edit.html', {'data': report_array, 'emp_id': emp_code})
        else:
            update_messages = request.session['UPDATE_EMP_SALARY_DETAILS']
            del request.session["UPDATE_EMP_SALARY_DETAILS"]

            request.session.modified = True

            return render(request, 'Employee_salary_edit.html', {'update_messages': update_messages})


def screenshots_as_list(salary_details):
    class details_class:
        NET_PAY = salary_details.NET_PAY
        SALARY_UPDATE_DATE = salary_details.SALARY_UPDATE_DATE
        TOTAL_EARN = salary_details.TOTAL_EARN
        TOTAL_DEDUCATION = salary_details.TOTAL_DEDUCATION
        print("******", TOTAL_EARN)
        FIXED_SALARY = salary_details.FIXED_SALARY
        FIXED_SALARY_CHECK = salary_details.FIXED_SALARY
        BASIC = salary_details.BASIC
        BASI_CHECK = salary_details.BASIC
        DEARANCE_ALLOWANCES = salary_details.DEARANCE_ALLOWANCES
        DEARANCE_ALLOWANCES_CHECK = salary_details.DEARANCE_ALLOWANCES
        SPECIAL_ALLOWANCES = salary_details.SPECIAL_ALLOWANCES
        SPECIAL_ALLOWANCES_CHECK = salary_details.SPECIAL_ALLOWANCES
        HOUSE_RENT_ALLOWANCES = salary_details.HOUSE_RENT_ALLOWANCES
        HOUSE_RENT_ALLOWANCES_CHECK = salary_details.HOUSE_RENT_ALLOWANCES
        CONVEYANCE = salary_details.CONVEYANCE
        CONVEYANCE_CHECK = salary_details.CONVEYANCE
        OTHER_ALLOWANCES = salary_details.OTHER_ALLOWANCES
        OTHER_ALLOWANCES_CHECK = salary_details.OTHER_ALLOWANCES
        OVERTIME_AMOUNT = salary_details.OVERTIME_AMOUNT
        OVERTIME_AMOUNT_CHECK = salary_details.OVERTIME_AMOUNT
        SITE_ALLOWANCES = salary_details.SITE_ALLOWANCES
        SITE_ALLOWANCES_CHECK = salary_details.SITE_ALLOWANCES
        SHIFT_ALLOWANCES_AMOUNT = salary_details.SHIFT_ALLOWANCES_AMOUNT
        SHIFT_ALLOWANCES_AMOUNT_CHECK = salary_details.SHIFT_ALLOWANCES_AMOUNT
        INCENTIVE = salary_details.INCENTIVE
        INCENTIVE_CHECK = salary_details.INCENTIVE
        LEAVE_TRAVEL_ALLOWANCES = salary_details.LEAVE_TRAVEL_ALLOWANCES
        LEAVE_TRAVEL_ALLOWANCES_CHECK = salary_details.LEAVE_TRAVEL_ALLOWANCES
        MEDICAL_ALLOWANCES = salary_details.MEDICAL_ALLOWANCES
        MEDICAL_ALLOWANCES_CHECK = salary_details.MEDICAL_ALLOWANCES
        CHILD_EDUCATIONS_ALLOWANCES = salary_details.CHILD_EDUCATIONS_ALLOWANCES
        CHILD_EDUCATIONS_ALLOWANCES_CHECK = salary_details.CHILD_EDUCATIONS_ALLOWANCES
        ATTENDANCE_BONUS = salary_details.ATTENDANCE_BONUS
        ATTENDANCE_BONUS_CHECK = salary_details.ATTENDANCE_BONUS
        ATTENDANCE_INCENTIVE = salary_details.ATTENDANCE_INCENTIVE
        ATTENDANCE_INCENTIVE_CHECK = salary_details.ATTENDANCE_INCENTIVE
        MONTHLY_BOUNS = salary_details.MONTHLY_BOUNS
        EXTRA_BOUNS = salary_details.EXTRA_BOUNS
        MONTHLY_BOUNS_CHECK = salary_details.MONTHLY_BOUNS
        MONTHLY_LEAVE_WAGES = salary_details.MONTHLY_LEAVE_WAGES
        PF = salary_details.PROVIDENT_FUND
        PF_CHECK = salary_details.PROVIDENT_FUND
        ESIC = salary_details.ESIC
        ESIC_CHECK = salary_details.ESIC
        MONTHLY_LEAVE_WAGES_CHECK = salary_details.MONTHLY_LEAVE_WAGES
        RELIVER_DUTY_WAGES = salary_details.RELIVER_DUTY_WAGES
        RELIVER_DUTY_WAGES_CHECK = salary_details.RELIVER_DUTY_WAGES
        ARREARS_WAGES = salary_details.ARREARS_WAGES
        PROVIDENT_FUND = salary_details.PROVIDENT_FUND
        ARREARS_WAGES_CHECK = salary_details.ARREARS_WAGES
        PROFESSIONAL_TAX = salary_details.PROFESSIONAL_TAX
        PROFESSIONAL_TAX_CHECK = salary_details.PROFESSIONAL_TAX
        LABOUR_WELFARE_FUND = salary_details.LABOUR_WELFARE_FUND
        LABOUR_WELFARE_FUND_CHECK = salary_details.LABOUR_WELFARE_FUND
        INCOME_TAX = salary_details.INCOME_TAX
        INCOME_TAX_CHECK = salary_details.INCOME_TAX
        LOAN = salary_details.LOAN
        LOAN_CHECK = salary_details.LOAN
        SALARY_ADVANCE = salary_details.SALARY_ADVANCE
        SALARY_ADVANCE_CHECK = salary_details.SALARY_ADVANCE
        OTHER_DEDUCTION = salary_details.OTHER_DEDUCTION
        OTHER_DEDUCTION_CHECK = salary_details.OTHER_DEDUCTION
        UNIFORM_DEDUCTION = salary_details.UNIFORM_DEDUCTION
        UNIFORM_DEDUCTION_CHECK = salary_details.UNIFORM_DEDUCTION

    return details_class
