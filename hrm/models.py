from django.db import models
# Create your models here.
from datetime import date


class New_Emp(models.Model):
    ID = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=120, default="")
    emp_code = models.CharField(max_length=120, default="")
    dob = models.CharField(max_length=25, default="")
    gender = models.CharField(max_length=10, default="")
    country = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    district = models.CharField(max_length=100, default="")
    branch = models.CharField(max_length=120, default="")
    area = models.CharField(max_length=120, default="")
    client = models.CharField(max_length=120, default="")
    unit = models.CharField(max_length=120, default="")
    salutation = models.CharField(max_length=120, default="")
    doj = models.CharField(max_length=25, default="")
    bdsb = models.CharField(max_length=25, default="")
    designation = models.CharField(max_length=120, default="")
    marital_status = models.CharField(max_length=50, default="")
    wife_husband = models.CharField(max_length=120, default="")
    father_name = models.CharField(max_length=120, default="")
    mother_name = models.CharField(max_length=120, default="")
    category = models.CharField(max_length=120, default="")
    higher_edu = models.CharField(max_length=100, default="")
    birth_place = models.CharField(max_length=120, default="")
    pan_no = models.CharField(max_length=120, default="")
    pf_no = models.CharField(max_length=120, default="")
    esi_no = models.CharField(max_length=120, default="")
    aadhar_no = models.CharField(max_length=120, default="")
    uan_no = models.CharField(max_length=120, default="")
    id_card_no = models.CharField(max_length=120, default="")
    permanet = models.CharField(max_length=20, default="")
    issue_date = models.CharField(max_length=25, default="")
    valid_date = models.CharField(max_length=25, default="")
    nationality = models.CharField(max_length=120, default="")
    name_of_police_thana = models.CharField(max_length=120, default="")
    DATE = models.DateField(default=date.today)

    def __str__(self):
        return self.EMP_CODE


class EMP_INCREMENT_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    OLD_SALARY = models.CharField(max_length=100, default="")
    INCREMENT_AMOUNT = models.CharField(max_length=100, default="")
    CURRENT_SALARY = models.CharField(max_length=100, default="")
    INCREMENT_PURPOSE = models.CharField(max_length=200, default="")
    INCREMENT_UPDATE_DATE = models.CharField(max_length=100, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_increment_details"


class EMP_EXPENSE_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    EXPENSE_DATE = models.CharField(max_length=100, default="")
    EXPENSE_AMOUNT = models.CharField(max_length=100, default="")
    EXPENSE_PURPOSE = models.CharField(max_length=100, default="")
    REMARK = models.CharField(max_length=200, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_expense_details"


class EMP_CERTIFICATE_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    CERTIFICATE_TYPE = models.CharField(max_length=100, default="")
    CERTIFICATE_DESCRIPTION = models.CharField(max_length=200, default="")
    ADD_DATE = models.CharField(max_length=100, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_certificate_details"


class EMP_BONUS_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    BONUS_NAME = models.CharField(max_length=100, default="")
    BONUS_AMOUNT = models.CharField(max_length=100, default="")
    BONUS_DESCRIPTION = models.CharField(max_length=200, default="")
    BONUS_UPDATE_DATE = models.CharField(max_length=100, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_bonus_details"


class EMP_DAILY_ATTENDANCE_UPDATED(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    IN_TIME = models.CharField(max_length=100, default="")
    OUT_TIME = models.CharField(max_length=100, default="")
    ATTENDANCE_STATUS = models.CharField(max_length=200, default="")
    LAST_UPDATE_DATE = models.CharField(max_length=100, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_daily_attendance_updated"


class EMP_AWARD_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    AWARD_CATEGORY = models.CharField(max_length=100, default="")
    GIFT = models.CharField(max_length=100, default="")
    AWARD_MONTH = models.CharField(max_length=100, default="")
    AWARD_DESCRIPTION = models.CharField(max_length=100, default="")
    AWARD_STATUS = models.CharField(max_length=200, default="")
    AWARD_ADD_DATE = models.CharField(max_length=100, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_award_list"


class LEAVE_CATEGORY_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    CATEGORY_NAME = models.CharField(max_length=150, default="")
    CATEGORY_DESCRIPTION = models.CharField(max_length=150, default="")
    STATUS = models.CharField(max_length=150, default="")
    ADDED_DATE = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.CATEGORY_NAME

    class Meta:
        db_table = "leave_category_list"


class LEAVE_APPLICATION_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    REASON = models.CharField(max_length=150, default="")
    START_DATE = models.CharField(max_length=150, default="")
    END_DATE = models.CharField(max_length=150, default="")
    LEAVE_CATEGORY = models.CharField(max_length=150, default="")
    LEAVE_DAYS = models.CharField(max_length=150, default="")
    STATUS = models.CharField(max_length=150, default="")
    ADDED_DATE = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.CATEGORY_NAME

    class Meta:
        db_table = "leave_application_list"


class NOTICE_BOARD(models.Model):
    ID = models.AutoField(primary_key=True)
    TITLE = models.CharField(max_length=120, default="")
    DESCRIPTION = models.CharField(max_length=600, default="")
    CREATED_AT = models.CharField(max_length=150, default="")
    STATUS = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.TITLE

    class Meta:
        db_table = "notice_board"


class HOLIDAYS(models.Model):
    ID = models.AutoField(primary_key=True)
    HOLIDAY_NAME = models.CharField(max_length=120, default="")
    DESCRIPTION = models.CharField(max_length=600, default="")
    HOLIDAY_DATE = models.CharField(max_length=150, default="")
    STATUS = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.HOLIDAY_NAME

    class Meta:
        db_table = "holidays"


class CLIENT_TYPE(models.Model):
    ID = models.AutoField(primary_key=True)
    CLIENT_TYPE = models.CharField(max_length=120, default="")
    DESCRIPTION = models.CharField(max_length=600, default="")
    CREATED_AT = models.CharField(max_length=150, default="")
    STATUS = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.CLIENT_TYPE

    class Meta:
        db_table = "client_type"


class PERSONAL_EVENT(models.Model):
    ID = models.AutoField(primary_key=True)
    EVENT_NAME = models.CharField(max_length=120, default="")
    START_DATE = models.CharField(max_length=120, default="")
    END_DATE = models.CharField(max_length=120, default="")
    DESCRIPTION = models.CharField(max_length=600, default="")
    CREATED_AT = models.CharField(max_length=150, default="")
    STATUS = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EVENT_NAME

    class Meta:
        db_table = "personal_event"


class ATTENDANCE_SETTING(models.Model):
    ID = models.AutoField(primary_key=True)
    ATTENDANCE_SETTING = models.CharField(max_length=120, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EVENT_NAME

    class Meta:
        db_table = "attendance_setting"


class WORKING_DAY(models.Model):
    ID = models.AutoField(primary_key=True)
    SUNDAY = models.CharField(max_length=120, default="")
    MONDAY = models.CharField(max_length=120, default="")
    TUESDAY = models.CharField(max_length=120, default="")
    WEDNESDAY = models.CharField(max_length=120, default="")
    THURSDAY = models.CharField(max_length=120, default="")
    FRIDAY = models.CharField(max_length=120, default="")
    SATURDAY = models.CharField(max_length=120, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EVENT_NAME

    class Meta:
        db_table = "working_day"


class AWARD_CATEGORY_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    AWARD_CATEGORY = models.CharField(max_length=120, default="")
    CREATED_AT = models.CharField(max_length=150, default="")
    STATUS = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.AWARD_CATEGORY

    class Meta:
        db_table = "award_category_list"


class DESIGNATION_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    DESIGNATION = models.CharField(max_length=120, default="")
    CREATED_AT = models.CharField(max_length=150, default="")
    DESCRIPTION = models.CharField(max_length=300, default="")
    STATUS = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.AWARD_CATEGORY

    class Meta:
        db_table = "designation_list"


class MANAGE_FOLDERS(models.Model):
    ID = models.AutoField(primary_key=True)
    FOLDER_NAME = models.CharField(max_length=120, default="")
    DESCRIPTION = models.CharField(max_length=300, default="")
    CREATED_AT = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.FOLDER_NAME

    class Meta:
        db_table = "manage_folder"


class MANAGE_FILES(models.Model):
    ID = models.AutoField(primary_key=True)
    FOLDER_NAME = models.CharField(max_length=120, default="")
    CAPTION = models.CharField(max_length=120, default="")
    UPLOAD_FILE = models.CharField(max_length=300, default="")
    UPLOAD_FILE_URL = models.CharField(max_length=300, default="")
    CREATED_AT = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.FOLDER_NAME

    class Meta:
        db_table = "manage_files"


class MONTHLY_ATTENDANCE_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    TOTAL_PRESENT = models.CharField(max_length=150, default="")
    TOTAL_ABSENT = models.CharField(max_length=150, default="")
    TOTAL_LEAVE = models.CharField(max_length=150, default="")
    MONTH_YEAR = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "monthly_attendance_details"


class EXPENSE_CATEGORY_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    EXP_PURPOSE = models.CharField(max_length=150, default="")
    CREATED_BY = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EXP_PURPOSE

    class Meta:
        db_table = "expense_category_list"


class EMP_DAILY_ATTENDANCE_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    IN_TIME = models.CharField(max_length=100, default="")
    OUT_TIME = models.CharField(max_length=100, default="")
    ATTENDANCE_STATUS = models.CharField(max_length=200, default="")
    ATTENDANCE_DATE = models.CharField(max_length=100, default="")
    ATTENDANCE_MONTH = models.CharField(max_length=100, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_daily_attendance_list"


class EMP_LOAN_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    LOAN_NAME = models.CharField(max_length=100, default="")
    LOAN_AMOUNT = models.CharField(max_length=100, default="")
    NUMBER_OF_INSTALLMENT = models.CharField(max_length=100, default="")
    AMOUNT_OF_INSTALLMENT = models.CharField(max_length=100, default="")
    REMAINING_OF_INSTALLMENT = models.CharField(max_length=100, default="")
    LOAN_DESCRIPTION = models.CharField(max_length=200, default="")
    LOAN_ADDED_DATE = models.CharField(max_length=100, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_loan_details"


class EMP_ADVANCE_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=120, default="")
    EMP_NAME = models.CharField(max_length=150, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    ADVANCE_AMOUNT = models.CharField(max_length=100, default="")
    REMAINING_AMOUNT = models.CharField(max_length=100, default="")
    GIVEN_AMOUNT = models.CharField(max_length=100, default="")
    GIVING_AMOUNT = models.CharField(max_length=100, default="")
    LAST_ADVANCE_UPDATED = models.CharField(max_length=100, default="")
    ADVANCE_ADDED_DATE = models.CharField(max_length=100, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_advance_details"


class Edit_Url(models.Model):
    ID = models.AutoField(primary_key=True)
    IMAGE_URL = models.CharField(max_length=150)
    DOCUMENT_URL = models.CharField(max_length=150)
    TIMESTAMP = models.DateField(default=date.today)

    class Meta:
        db_table = "document_url"


class new_emp_reg(models.Model):
    ID = models.AutoField(primary_key=True, db_index=True)
    EMP_NAME = models.CharField(max_length=150, default="")
    EMP_CODE = models.CharField(max_length=150, default="")
    DOB = models.CharField(max_length=50, default="")
    GENDER = models.CharField(max_length=15, default="")
    REG_DATE = models.CharField(max_length=50, default="")
    REG_TIME = models.CharField(max_length=50, default="")
    SALUTATION = models.CharField(max_length=10, default="")
    USER_TYPE = models.CharField(max_length=25, default="")
    MARITAL_STATUS = models.CharField(max_length=50)
    MOBILE_NO = models.CharField(max_length=12, default="")
    AGE = models.CharField(max_length=12, default="")
    EXPERIANCE = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __unicode__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_register"


class EMP_COMPANY_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True, db_index=True)
    EMP_CODE = models.CharField(max_length=150)
    EMP_LINK = models.ForeignKey(new_emp_reg, default=1, verbose_name="emp_link", on_delete=models.SET_DEFAULT)
    COUNTRY = models.CharField(max_length=150, default="")
    STATE = models.CharField(max_length=150, default="")
    DISTRICT = models.CharField(max_length=150, default="")
    BRANCH = models.CharField(max_length=150, default="")
    AREA = models.CharField(max_length=150, default="")
    CLIENT = models.CharField(max_length=150, default="")
    UNIT = models.CharField(max_length=150, default="")
    DATE_OF_JOIN = models.CharField(max_length=50, default="")
    BIO_DATE_SUB_DATE = models.CharField(max_length=50, default="")
    DESIGNATION = models.CharField(max_length=150, default="")
    CATEGORY = models.CharField(max_length=150, default="")
    ISSUE_DATE = models.CharField(max_length=50, default="")
    VAILD_DATE = models.CharField(max_length=50, default="")
    DATE_OF_EXIT = models.CharField(max_length=50, default="")
    VAILD_DATE = models.CharField(max_length=50, default="")
    REASON_OF_EXIT = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        managed = True
        db_table = "emp_company_register"


class EMP_PERSONAL_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True, db_index=True)
    EMP_CODE = models.CharField(max_length=150)
    EMP_LINK = models.ForeignKey(EMP_COMPANY_DETAILS, default=1, verbose_name="emp_link", on_delete=models.SET_DEFAULT)
    WIFE_HUSBAND_NAME = models.CharField(max_length=150, default="")
    FATHER_NAME = models.CharField(max_length=150, default="")
    MOTHER_NAME = models.CharField(max_length=150, default="")
    HIGHEST_EDUCATION = models.CharField(max_length=150, default="")
    BIRTH_PLACE = models.CharField(max_length=150, default="")
    PAN_NO = models.CharField(max_length=150, default="")
    PF_NO = models.CharField(max_length=150, default="")
    ESI_NO = models.CharField(max_length=150, default="")
    AADHAR_NO = models.CharField(max_length=50, default="")
    UAN_NO = models.CharField(max_length=150, default="")
    ID_CARD_NO = models.CharField(max_length=150, default="")
    NATIONALITY = models.CharField(max_length=50, default="")
    BLOOD_GROUP = models.CharField(max_length=25, default="")
    SHOE_SIZE = models.CharField(max_length=10, default="")
    WAIST = models.CharField(max_length=10, default="")
    HEIGHT = models.CharField(max_length=10, default="")
    WEIGHT = models.CharField(max_length=10, default="")
    CHEST = models.CharField(max_length=10, default="")
    T_SHIRT_SIZE = models.CharField(max_length=10, default="")
    THOUSER_SIZE = models.CharField(max_length=10, default="")
    PROFILE_URL = models.CharField(max_length=200, default="")
    DOCUMENT_URL = models.CharField(max_length=200, default="")
    MARK_OF_IDENTIFICATION = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        managed = True
        db_table = "emp_personal_details"


class EMP_COMMUNICATION_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True, db_index=True)
    EMP_CODE = models.CharField(max_length=150)
    EMP_LINK = models.ForeignKey(EMP_PERSONAL_DETAILS, default=1, verbose_name="emp_link", on_delete=models.SET_DEFAULT)
    ADDRESS = models.TextField(default="")
    STREET = models.CharField(max_length=150, default="")
    DISTRICT = models.CharField(max_length=150, default="")
    PINCODE = models.CharField(max_length=50, default="")
    TELEPHONE = models.CharField(max_length=15, default="")
    MOBILE_NO = models.CharField(max_length=50, default="")
    EMAIL_ID = models.CharField(max_length=150, default="")
    DURATION = models.CharField(max_length=150, default="")
    STATE = models.CharField(max_length=50, default="")
    PER_ADDRESS = models.TextField(default="")
    PER_STREET = models.CharField(max_length=150, default="")
    PER_DISTRICT = models.CharField(max_length=150, default="")
    PER_PINCODE = models.CharField(max_length=50, default="")
    PER_DURATION = models.CharField(max_length=150, default="")
    PER_STATE = models.CharField(max_length=50, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        managed = True
        db_table = "emp_communication_details"


class EMP_BANK_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True, db_index=True)
    EMP_CODE = models.CharField(max_length=150)
    EMP_LINK = models.ForeignKey(EMP_COMMUNICATION_DETAILS, default=1, verbose_name="emp_link",
                                 on_delete=models.SET_DEFAULT)
    ACCOUNT_NO = models.CharField(max_length=150, default="")
    BANK_NAME = models.CharField(max_length=150, default="")
    IFSC_CODE = models.CharField(max_length=50, default="")
    BRANCH = models.CharField(max_length=50, default="")
    PAYMENT_MODE = models.CharField(max_length=50, default="")
    PASSBOOK_NAME = models.CharField(max_length=150, default="")
    JOIN_ACC_NO = models.CharField(max_length=150, default="")
    JOIN_ACC_NAME = models.CharField(max_length=150, default="")
    JOIN_ACC_BRANCH_NAME = models.CharField(max_length=150, default="")
    JOIN_ACC_BANK_NAME = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        managed = True
        db_table = "emp_bank_details"


class salary_details(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=50)
    EMP_LINK = models.ForeignKey(EMP_BANK_DETAILS, default=1, verbose_name="emp_link",
                                 on_delete=models.SET_DEFAULT)
    FIXED_SALARY = models.CharField(max_length=150, default="")
    MONTH_SALARY = models.CharField(max_length=150, default="")
    BASIC = models.CharField(max_length=150, default="")
    DEARANCE_ALLOWANCES = models.CharField(max_length=150, default="")
    SPECIAL_ALLOWANCES = models.CharField(max_length=150, default="")
    HOUSE_RENT_ALLOWANCES = models.CharField(max_length=150, default="")
    CONVEYANCE = models.CharField(max_length=150, default="")
    OTHER_ALLOWANCES = models.CharField(max_length=150, default="")
    OVERTIME_AMOUNT = models.CharField(max_length=150, default="")
    SITE_ALLOWANCES = models.CharField(max_length=150, default="")
    SHIFT_ALLOWANCES_AMOUNT = models.CharField(max_length=150, default="")
    INCENTIVE = models.CharField(max_length=150, default="")
    LEAVE_TRAVEL_ALLOWANCES = models.CharField(max_length=150, default="")
    MEDICAL_ALLOWANCES = models.CharField(max_length=150, default="")
    CHILD_EDUCATIONS_ALLOWANCES = models.CharField(max_length=150, default="")
    ATTENDANCE_BONUS = models.CharField(max_length=150, default="")
    ATTENDANCE_INCENTIVE = models.CharField(max_length=150, default="")
    MONTHLY_BOUNS = models.CharField(max_length=150, default="")
    EXTRA_BOUNS = models.CharField(max_length=150, default="")
    MONTHLY_LEAVE_WAGES = models.CharField(max_length=150, default="")
    PROFESSIONAL_TAX = models.CharField(max_length=150, default="")
    TOTAL_DEDUCATION = models.CharField(max_length=150, default="")
    TOTAL_EARN = models.CharField(max_length=150, default="")
    NET_PAY = models.CharField(max_length=150, default="")
    ESIC = models.CharField(max_length=150, default="")
    RELIVER_DUTY_WAGES = models.CharField(max_length=150, default="")
    ARREARS_WAGES = models.CharField(max_length=150, default="")
    PROVIDENT_FUND = models.CharField(max_length=150, default="")
    LABOUR_WELFARE_FUND = models.CharField(max_length=150, default="")
    PENSION_AMOUNT = models.CharField(max_length=150, default="")
    INCOME_TAX = models.CharField(max_length=150, default="")
    LOAN = models.CharField(max_length=150, default="")
    SALARY_ADVANCE = models.CharField(max_length=150, default="")
    OTHER_DEDUCTION = models.CharField(max_length=150, default="")
    UNIFORM_DEDUCTION = models.CharField(max_length=150, default="")
    SALARY_UPDATE_DATE = models.CharField(max_length=150, default="")
    NAMINE_E_NAME = models.CharField(max_length=150, default="")
    NAMINE_E_RELATIONS = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        managed = True
        db_table = "emp_salary_details"


class EMP_SALARY_MAINTAINS(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=50)
    FIXED_SALARY = models.CharField(max_length=150, default="")
    MONTH_SALARY = models.CharField(max_length=150, default="")
    BASIC = models.CharField(max_length=150, default="")
    DEARANCE_ALLOWANCES = models.CharField(max_length=150, default="")
    SPECIAL_ALLOWANCES = models.CharField(max_length=150, default="")
    HOUSE_RENT_ALLOWANCES = models.CharField(max_length=150, default="")
    CONVEYANCE = models.CharField(max_length=150, default="")
    OTHER_ALLOWANCES = models.CharField(max_length=150, default="")
    OVERTIME_AMOUNT = models.CharField(max_length=150, default="")
    SITE_ALLOWANCES = models.CharField(max_length=150, default="")
    SHIFT_ALLOWANCES_AMOUNT = models.CharField(max_length=150, default="")
    INCENTIVE = models.CharField(max_length=150, default="")
    LEAVE_TRAVEL_ALLOWANCES = models.CharField(max_length=150, default="")
    MEDICAL_ALLOWANCES = models.CharField(max_length=150, default="")
    CHILD_EDUCATIONS_ALLOWANCES = models.CharField(max_length=150, default="")
    ATTENDANCE_BONUS = models.CharField(max_length=150, default="")
    ATTENDANCE_INCENTIVE = models.CharField(max_length=150, default="")
    MONTHLY_BOUNS = models.CharField(max_length=150, default="")
    EXTRA_BOUNS = models.CharField(max_length=150, default="")
    MONTHLY_LEAVE_WAGES = models.CharField(max_length=150, default="")
    PROFESSIONAL_TAX = models.CharField(max_length=150, default="")
    PENSION_AMOUNT = models.CharField(max_length=150, default="")
    TOTAL_DEDUCATION = models.CharField(max_length=150, default="")
    TOTAL_EARN = models.CharField(max_length=150, default="")
    NET_PAY = models.CharField(max_length=150, default="")
    ESIC = models.CharField(max_length=150, default="")
    RELIVER_DUTY_WAGES = models.CharField(max_length=150, default="")
    ARREARS_WAGES = models.CharField(max_length=150, default="")
    PROVIDENT_FUND = models.CharField(max_length=150, default="")
    LABOUR_WELFARE_FUND = models.CharField(max_length=150, default="")
    INCOME_TAX = models.CharField(max_length=150, default="")
    LOAN = models.CharField(max_length=150, default="")
    SALARY_ADVANCE = models.CharField(max_length=150, default="")
    OTHER_DEDUCTION = models.CharField(max_length=150, default="")
    UNIFORM_DEDUCTION = models.CharField(max_length=150, default="")
    SALARY_UPDATE_DATE = models.CharField(max_length=150, default="")
    DAYS_PRESENT = models.CharField(max_length=150, default="")
    OVERTIME_HRS = models.CharField(max_length=150, default="")
    SHIFT_ALLOWANCES_HRS = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        managed = True
        db_table = "emp_salary_maintains"


class EMP_POLICE_VERFICATION(models.Model):
    ID = models.AutoField(primary_key=True, db_index=True)
    EMP_CODE = models.CharField(max_length=150)
    EMP_BANK = models.ForeignKey(EMP_BANK_DETAILS, default=1, verbose_name="emp_bank", on_delete=models.SET_DEFAULT)
    EMP_COMM = models.ForeignKey(EMP_COMMUNICATION_DETAILS, default=1, verbose_name="emp_com",
                                 on_delete=models.SET_DEFAULT)
    EMP_PER = models.ForeignKey(EMP_PERSONAL_DETAILS, default=1, verbose_name="emp_per", on_delete=models.SET_DEFAULT)
    EMP_COMPANY = models.ForeignKey(EMP_COMPANY_DETAILS, default=1, verbose_name="emp_company",
                                    on_delete=models.SET_DEFAULT)
    NEW_EMP = models.ForeignKey(new_emp_reg, default=1, verbose_name="new_emp", on_delete=models.SET_DEFAULT)
    EMP_SAL = models.ForeignKey(salary_details, default=1, verbose_name="emp_sal", on_delete=models.SET_DEFAULT)
    VERFICATION_NO = models.CharField(max_length=150, default="")
    VERFICATION_DATE = models.CharField(max_length=150, default="")
    CRIMINOLOGY = models.CharField(max_length=150, default="")
    PV_SEND_DATE = models.CharField(max_length=50, default="")
    PV_RETURN_DATE = models.CharField(max_length=50, default="")
    NAME_OF_POLICE_THANA = models.CharField(max_length=50, default="")
    IDENTITY_SIGN = models.CharField(max_length=150, default="")
    PV_VALID_UPTO = models.CharField(max_length=150, default="")
    REMARK_BY_THANA = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        managed = True
        db_table = "emp_verfication_details"


class BANK_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    BANK_NAME = models.CharField(max_length=150, default="")

    class Meta:
        db_table = "bank_name_list"


class Country(models.Model):
    ID = models.AutoField(primary_key=True)
    Country_Name = models.CharField(max_length=200)

    def __str__(self):
        return self.Country_Name

    class Meta:
        db_table = "country_table"


class State(models.Model):
    ID = models.AutoField(primary_key=True)
    State_Name = models.CharField(max_length=200)
    Country = models.ForeignKey("Country", on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return self.State_Name

    class Meta:
        db_table = "state_table"


class COUNTRY_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    COUNTRY_NAME = models.CharField(max_length=200)

    class Meta:
        db_table = "country_list"


class STATE_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    STATE_ID = models.CharField(max_length=50, default="")
    STATE_NAME = models.CharField(max_length=200, default="")
    COUNTRY_NAME = models.CharField(max_length=200, default="")

    class Meta:
        db_table = "state_list"


class CITY_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    CITY_ID = models.CharField(max_length=15, default="")
    CITY_NAME = models.CharField(max_length=200, default="")
    STATE_NAME = models.CharField(max_length=200, default="")
    COUNTRY_NAME = models.CharField(max_length=200, default="")

    class Meta:
        db_table = "city_list"


class CLIENT_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    CLIENT = models.CharField(max_length=200)

    class Meta:
        db_table = "client_list"


class UNIT_LIST(models.Model):
    ID = models.AutoField(primary_key=True)
    UNIT_ID = models.CharField(max_length=50, default="")
    UNIT = models.CharField(max_length=200, default="")
    CLIENT = models.CharField(max_length=200, default="")

    class Meta:
        db_table = "unit_list"


class CLIENT_DETAILS(models.Model):
    ID = models.AutoField(primary_key=True)
    CLIENT_ID = models.CharField(max_length=200, default="")
    CLIENT = models.CharField(max_length=200, default="")
    COUNTRY_NAME = models.CharField(max_length=200, default="")
    STATE_NAME = models.CharField(max_length=200, default="")
    DISTRICT_NAME = models.CharField(max_length=200, default="")
    BRANCH_NAME = models.CharField(max_length=200, default="")
    AREA_NAME = models.CharField(max_length=200, default="")
    UNIT = models.CharField(max_length=200, default="")
    E_MAIL = models.CharField(max_length=200, default="")
    WEB = models.CharField(max_length=200, default="")
    CONTACT_NO = models.CharField(max_length=200, default="")
    ADDRESS = models.CharField(max_length=200, default="")

    class Meta:
        db_table = "client_details"


class City(models.Model):
    ID = models.AutoField(primary_key=True)
    City_Name = models.CharField(max_length=200)
    Country = models.ForeignKey("State", on_delete=models.CASCADE, related_name='city')

    def __str__(self):
        return self.City_Name

    class Meta:
        db_table = "city_table"


class Client(models.Model):
    ID = models.AutoField(primary_key=True)
    Client_Name = models.CharField(max_length=500)

    def __str__(self):
        return self.Client_Name

    class Meta:
        db_table = "client_table"


class Unit(models.Model):
    ID = models.AutoField(primary_key=True)
    Unit_Name = models.CharField(max_length=200)
    Client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name='Unit')

    def __str__(self):
        return self.Unit_Name

    class Meta:
        db_table = "unit_table"


class Admin_Table(models.Model):
    ID = models.AutoField(primary_key=True)
    ADMIN_NAME = models.CharField(max_length=200)
    ADMIN_ID = models.IntegerField(default=0)

    def __str__(self):
        return self.ADMIN_ID

    class Meta:
        db_table = "admin_table"


class Monthly_Attendance_Table(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=50)
    DAYS_PRESENT = models.IntegerField(default=0)
    OVERTIME_HRS = models.IntegerField(default=0)
    SHIFT_ALLOWANCES_HRS = models.IntegerField(default=0)
    YEAR = models.CharField(max_length=25, default="")
    MONTH = models.CharField(max_length=25, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_monthly_attendance_table"


class New_Customer_Reg(models.Model):
    ID = models.AutoField(primary_key=True)
    CLIENT_CODE = models.CharField(max_length=50)
    CLIENT_NAME = models.CharField(max_length=50)
    EMAIL = models.CharField(max_length=150, default="")
    DOB = models.CharField(max_length=150, default="")
    CONTACT_NO = models.CharField(max_length=50, default="")
    WEB = models.CharField(max_length=25, default="")
    GENTER = models.CharField(max_length=25, default="")
    EMERGENCY_CONTACT_NO = models.CharField(max_length=50, default="")
    ADDRESS = models.CharField(max_length=150, default="")
    REG_DATE = models.CharField(max_length=50)
    REG_TIME = models.CharField(max_length=50)
    CLIENT_TYPE = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.CLIENT_CODE

    class Meta:
        db_table = "customer_register"


class Loan_Table(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=50)
    EMP_NAME = models.CharField(max_length=50)
    LOAN_TYPE = models.CharField(max_length=25, default="")
    LOAN_AMOUNT = models.IntegerField(default=0)
    NO_OF_INSTALLMENT = models.IntegerField(default=0)
    CLIENT = models.CharField(max_length=150, default="")
    UNIT = models.CharField(max_length=150, default="")
    APPLY_DATE = models.CharField(max_length=25, default="")
    CLOSE_DATE = models.CharField(max_length=25, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_loan_table"


class USER_REGISTER_TABLE(models.Model):
    ID = models.AutoField(primary_key=True)
    USER_NAME = models.CharField(max_length=50)
    PASSWORD = models.CharField(max_length=300)
    E_MAIL = models.CharField(max_length=125, default="")
    REGISTER_DATE = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    class Meta:
        db_table = "user_register_table"


"""class Bonus_Table(models.Model):
    ID = models.AutoField(primary_key=True)
    EMP_CODE = models.CharField(max_length=50)
    EMP_NAME = models.CharField(max_length=50)
    EMP_ID = models.IntegerField(default=0)
    FATHER_NAME = models.CharField(max_length=50, default="")
    CRYSTAL_JUBILEE = models.IntegerField(default=0)
    DESIGNATION = models.IntegerField(default=0)
    NO_DAYS_WORKED_INYEAR = models.CharField(max_length=150, default="")
    TOTAL_SALARY = models.CharField(max_length=50, default="")
    AMT_OF_BONUS = models.CharField(max_length=50, default="")
    PUJA_BONUS = models.CharField(max_length=50, default="")
    INTERIM_BONUS = models.CharField(max_length=50, default="")
    DEDUCTION_AMOUNT = models.IntegerField(default=0)
    TOTAL_SUM_DEDU = models.IntegerField(default=0)
    NET_AMOUNT = models.IntegerField(default=0)
    AMOUNT_PAID = models.IntegerField(default=0)
    PAID_DATE = models.CharField(max_length=50, default="")
    SIGNATURE = models.CharField(max_length=50, default="")
    CLIENT = models.CharField(max_length=150, default="")
    UNIT = models.CharField(max_length=150, default="")
    TIMESTAMP = models.DateTimeField(max_length=50, auto_now_add=True)

    def __str__(self):
        return self.EMP_CODE

    class Meta:
        db_table = "emp_loan_table" """
