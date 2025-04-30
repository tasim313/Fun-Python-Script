# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class LlxAbbreviations(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey('LlxUser', models.DO_NOTHING, blank=True, null=True)
    abbreviation_key = models.CharField(max_length=255, blank=True, null=True)
    abbreviation_full_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_abbreviations'
        unique_together = (('fk_user', 'abbreviation_key'),)


class LlxAccountingAccount(models.Model):
    rowid = models.BigAutoField(primary_key=True)
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_pcg_version = models.ForeignKey('LlxAccountingSystem', models.DO_NOTHING, db_column='fk_pcg_version', to_field='pcg_version')
    pcg_type = models.CharField(max_length=20)
    account_number = models.CharField(max_length=32)
    account_parent = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255)
    labelshort = models.CharField(max_length=255, blank=True, null=True)
    fk_accounting_category = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    active = models.SmallIntegerField()
    reconcilable = models.SmallIntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_accounting_account'
        unique_together = (('account_number', 'entity', 'fk_pcg_version'),)


class LlxAccountingAccountHistory(models.Model):
    history_id = models.BigAutoField(primary_key=True)
    rowid = models.BigIntegerField()
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField(blank=True, null=True)
    fk_pcg_version = models.CharField(max_length=32)
    pcg_type = models.CharField(max_length=20)
    account_number = models.CharField(max_length=32)
    account_parent = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255)
    labelshort = models.CharField(max_length=255, blank=True, null=True)
    fk_accounting_category = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    active = models.SmallIntegerField()
    reconcilable = models.SmallIntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    operation = models.CharField(max_length=10)
    operation_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_accounting_account_history'


class LlxAccountingBookkeeping(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    piece_num = models.IntegerField()
    doc_date = models.DateField()
    doc_type = models.CharField(max_length=30)
    doc_ref = models.CharField(max_length=300)
    fk_doc = models.IntegerField()
    fk_docdet = models.IntegerField()
    thirdparty_code = models.CharField(max_length=32, blank=True, null=True)
    subledger_account = models.CharField(max_length=32, blank=True, null=True)
    subledger_label = models.CharField(max_length=255, blank=True, null=True)
    numero_compte = models.CharField(max_length=32)
    label_compte = models.CharField(max_length=255)
    label_operation = models.CharField(max_length=255, blank=True, null=True)
    debit = models.DecimalField(max_digits=24, decimal_places=8)
    credit = models.DecimalField(max_digits=24, decimal_places=8)
    montant = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    sens = models.CharField(max_length=1, blank=True, null=True)
    multicurrency_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_code = models.CharField(max_length=255, blank=True, null=True)
    lettering_code = models.CharField(max_length=255, blank=True, null=True)
    date_lettering = models.DateTimeField(blank=True, null=True)
    date_lim_reglement = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user = models.IntegerField(blank=True, null=True)
    code_journal = models.CharField(max_length=32)
    journal_label = models.CharField(max_length=255, blank=True, null=True)
    date_validated = models.DateTimeField(blank=True, null=True)
    date_export = models.DateTimeField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_accounting_bookkeeping'


class LlxAccountingBookkeepingTmp(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    doc_date = models.DateField()
    doc_type = models.CharField(max_length=30)
    doc_ref = models.CharField(max_length=300)
    fk_doc = models.IntegerField()
    fk_docdet = models.IntegerField()
    thirdparty_code = models.CharField(max_length=32, blank=True, null=True)
    subledger_account = models.CharField(max_length=32, blank=True, null=True)
    subledger_label = models.CharField(max_length=255, blank=True, null=True)
    numero_compte = models.CharField(max_length=32, blank=True, null=True)
    label_compte = models.CharField(max_length=255)
    label_operation = models.CharField(max_length=255, blank=True, null=True)
    debit = models.DecimalField(max_digits=24, decimal_places=8)
    credit = models.DecimalField(max_digits=24, decimal_places=8)
    montant = models.DecimalField(max_digits=24, decimal_places=8)
    sens = models.CharField(max_length=1, blank=True, null=True)
    multicurrency_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_code = models.CharField(max_length=255, blank=True, null=True)
    lettering_code = models.CharField(max_length=255, blank=True, null=True)
    date_lettering = models.DateTimeField(blank=True, null=True)
    date_lim_reglement = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user = models.IntegerField(blank=True, null=True)
    code_journal = models.CharField(max_length=32)
    journal_label = models.CharField(max_length=255, blank=True, null=True)
    piece_num = models.IntegerField()
    date_validated = models.DateTimeField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_accounting_bookkeeping_tmp'


class LlxAccountingFiscalyear(models.Model):
    rowid = models.AutoField(primary_key=True)
    label = models.CharField(max_length=128)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    statut = models.SmallIntegerField()
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_accounting_fiscalyear'


class LlxAccountingGroupsAccount(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_accounting_account = models.IntegerField()
    fk_c_accounting_category = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_accounting_groups_account'


class LlxAccountingJournal(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    code = models.CharField(max_length=32)
    label = models.CharField(max_length=128)
    nature = models.SmallIntegerField()
    active = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_accounting_journal'
        unique_together = (('code', 'entity'),)


class LlxAccountingSystem(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_country = models.IntegerField(blank=True, null=True)
    pcg_version = models.CharField(unique=True, max_length=32)
    label = models.CharField(max_length=128)
    active = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_accounting_system'


class LlxActioncomm(models.Model):
    ref = models.CharField(max_length=30)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField()
    datep = models.DateTimeField(blank=True, null=True)
    datep2 = models.DateTimeField(blank=True, null=True)
    fk_action = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_mod = models.IntegerField(blank=True, null=True)
    fk_project = models.IntegerField(blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_contact = models.IntegerField(blank=True, null=True)
    fk_parent = models.IntegerField()
    fk_user_action = models.IntegerField(blank=True, null=True)
    fk_user_done = models.IntegerField(blank=True, null=True)
    transparency = models.IntegerField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True)
    visibility = models.CharField(max_length=12, blank=True, null=True)
    fulldayevent = models.SmallIntegerField()
    percent = models.SmallIntegerField()
    location = models.CharField(max_length=128, blank=True, null=True)
    durationp = models.FloatField(blank=True, null=True)
    label = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)
    calling_duration = models.IntegerField(blank=True, null=True)
    email_subject = models.CharField(max_length=255, blank=True, null=True)
    email_msgid = models.CharField(max_length=255, blank=True, null=True)
    email_from = models.CharField(max_length=255, blank=True, null=True)
    email_sender = models.CharField(max_length=255, blank=True, null=True)
    email_to = models.CharField(max_length=255, blank=True, null=True)
    email_tocc = models.CharField(max_length=255, blank=True, null=True)
    email_tobcc = models.CharField(max_length=255, blank=True, null=True)
    errors_to = models.CharField(max_length=255, blank=True, null=True)
    reply_to = models.CharField(max_length=255, blank=True, null=True)
    recurid = models.CharField(max_length=128, blank=True, null=True)
    recurrule = models.CharField(max_length=128, blank=True, null=True)
    recurdateend = models.DateTimeField(blank=True, null=True)
    num_vote = models.IntegerField(blank=True, null=True)
    event_paid = models.SmallIntegerField()
    status = models.SmallIntegerField()
    fk_element = models.IntegerField(blank=True, null=True)
    elementtype = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_actioncomm'
        unique_together = (('ref', 'entity'),)


class LlxActioncommExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_actioncomm_extrafields'


class LlxActioncommReminder(models.Model):
    rowid = models.AutoField(primary_key=True)
    dateremind = models.DateTimeField(blank=True, null=True)
    typeremind = models.CharField(max_length=32)
    fk_user = models.IntegerField()
    offsetvalue = models.IntegerField()
    offsetunit = models.CharField(max_length=1)
    status = models.IntegerField()
    lasterror = models.CharField(max_length=128, blank=True, null=True)
    entity = models.IntegerField()
    fk_actioncomm = models.IntegerField()
    fk_email_template = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_actioncomm_reminder'
        unique_together = (('fk_actioncomm', 'fk_user', 'typeremind', 'offsetvalue', 'offsetunit'),)


class LlxActioncommResources(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_actioncomm = models.IntegerField()
    element_type = models.CharField(max_length=50)
    fk_element = models.IntegerField()
    answer_status = models.CharField(max_length=50, blank=True, null=True)
    mandatory = models.SmallIntegerField(blank=True, null=True)
    transparency = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_actioncomm_resources'
        unique_together = (('fk_actioncomm', 'element_type', 'fk_element'),)


class LlxAdherent(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=128, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    civility = models.CharField(max_length=6, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    login = models.CharField(max_length=50, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=50, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    pass_crypted = models.CharField(max_length=128, blank=True, null=True)
    fk_adherent_type = models.ForeignKey('LlxAdherentType', models.DO_NOTHING, db_column='fk_adherent_type')
    morphy = models.CharField(max_length=3)
    societe = models.CharField(max_length=128, blank=True, null=True)
    fk_soc = models.OneToOneField('LlxSociete', models.DO_NOTHING, db_column='fk_soc', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip = models.CharField(max_length=30, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    country = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    socialnetworks = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    phone_perso = models.CharField(max_length=30, blank=True, null=True)
    phone_mobile = models.CharField(max_length=30, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    statut = models.SmallIntegerField()
    public = models.SmallIntegerField()
    datefin = models.DateTimeField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    datevalid = models.DateTimeField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_mod = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    canvas = models.CharField(max_length=32, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_adherent'
        unique_together = (('login', 'entity'), ('ref', 'entity'),)


class LlxAdherentExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_adherent_extrafields'


class LlxAdherentType(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    tms = models.DateTimeField()
    statut = models.SmallIntegerField()
    libelle = models.CharField(max_length=50)
    morphy = models.CharField(max_length=3)
    duration = models.CharField(max_length=6, blank=True, null=True)
    subscription = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    vote = models.CharField(max_length=3)
    note = models.TextField(blank=True, null=True)
    mail_valid = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_adherent_type'
        unique_together = (('libelle', 'entity'),)


class LlxAdherentTypeExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_adherent_type_extrafields'


class LlxAdherentTypeLang(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_type = models.IntegerField()
    lang = models.CharField(max_length=5)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_adherent_type_lang'


class LlxAsset(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=128)
    entity = models.IntegerField()
    label = models.CharField(max_length=255, blank=True, null=True)
    acquisition_value_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    recovered_vat = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat')
    fk_user_modif = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_modif', related_name='llxasset_fk_user_modif_set', blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    status = models.IntegerField()
    fk_asset_model = models.ForeignKey('LlxAssetModel', models.DO_NOTHING, db_column='fk_asset_model', blank=True, null=True)
    reversal_amount_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    reversal_date = models.DateField(blank=True, null=True)
    date_acquisition = models.DateField()
    date_start = models.DateField()
    qty = models.FloatField()
    acquisition_type = models.SmallIntegerField()
    asset_type = models.SmallIntegerField()
    not_depreciated = models.IntegerField(blank=True, null=True)
    disposal_date = models.DateField(blank=True, null=True)
    disposal_amount_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_disposal_type = models.ForeignKey('LlxCAssetDisposalType', models.DO_NOTHING, db_column='fk_disposal_type', blank=True, null=True)
    disposal_depreciated = models.IntegerField(blank=True, null=True)
    disposal_subject_to_vat = models.IntegerField(blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_asset'


class LlxAssetAccountancyCodesEconomic(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_asset = models.OneToOneField(LlxAsset, models.DO_NOTHING, db_column='fk_asset', blank=True, null=True)
    fk_asset_model = models.OneToOneField('LlxAssetModel', models.DO_NOTHING, db_column='fk_asset_model', blank=True, null=True)
    asset = models.CharField(max_length=32, blank=True, null=True)
    depreciation_asset = models.CharField(max_length=32, blank=True, null=True)
    depreciation_expense = models.CharField(max_length=32, blank=True, null=True)
    value_asset_sold = models.CharField(max_length=32, blank=True, null=True)
    receivable_on_assignment = models.CharField(max_length=32, blank=True, null=True)
    proceeds_from_sales = models.CharField(max_length=32, blank=True, null=True)
    vat_collected = models.CharField(max_length=32, blank=True, null=True)
    vat_deductible = models.CharField(max_length=32, blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_modif = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_modif', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_asset_accountancy_codes_economic'


class LlxAssetAccountancyCodesFiscal(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_asset = models.OneToOneField(LlxAsset, models.DO_NOTHING, db_column='fk_asset', blank=True, null=True)
    fk_asset_model = models.OneToOneField('LlxAssetModel', models.DO_NOTHING, db_column='fk_asset_model', blank=True, null=True)
    accelerated_depreciation = models.CharField(max_length=32, blank=True, null=True)
    endowment_accelerated_depreciation = models.CharField(max_length=32, blank=True, null=True)
    provision_accelerated_depreciation = models.CharField(max_length=32, blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_modif = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_modif', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_asset_accountancy_codes_fiscal'


class LlxAssetDepreciation(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_asset = models.ForeignKey(LlxAsset, models.DO_NOTHING, db_column='fk_asset')
    depreciation_mode = models.CharField(max_length=255)
    ref = models.CharField(max_length=255)
    depreciation_date = models.DateTimeField(blank=True, null=True)
    depreciation_ht = models.DecimalField(max_digits=24, decimal_places=8)
    cumulative_depreciation_ht = models.DecimalField(max_digits=24, decimal_places=8)
    accountancy_code_debit = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_credit = models.CharField(max_length=32, blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_modif = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_modif', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_asset_depreciation'
        unique_together = (('fk_asset', 'depreciation_mode', 'ref'),)


class LlxAssetDepreciationOptionsEconomic(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_asset = models.OneToOneField(LlxAsset, models.DO_NOTHING, db_column='fk_asset', blank=True, null=True)
    fk_asset_model = models.OneToOneField('LlxAssetModel', models.DO_NOTHING, db_column='fk_asset_model', blank=True, null=True)
    depreciation_type = models.SmallIntegerField()
    accelerated_depreciation_option = models.IntegerField(blank=True, null=True)
    degressive_coefficient = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    duration = models.SmallIntegerField()
    duration_type = models.SmallIntegerField()
    amount_base_depreciation_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    amount_base_deductible_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_amount_last_depreciation_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_modif = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_modif', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_asset_depreciation_options_economic'


class LlxAssetDepreciationOptionsFiscal(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_asset = models.OneToOneField(LlxAsset, models.DO_NOTHING, db_column='fk_asset', blank=True, null=True)
    fk_asset_model = models.OneToOneField('LlxAssetModel', models.DO_NOTHING, db_column='fk_asset_model', blank=True, null=True)
    depreciation_type = models.SmallIntegerField()
    degressive_coefficient = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    duration = models.SmallIntegerField()
    duration_type = models.SmallIntegerField()
    amount_base_depreciation_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    amount_base_deductible_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_amount_last_depreciation_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_modif = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_modif', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_asset_depreciation_options_fiscal'


class LlxAssetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_asset_extrafields'


class LlxAssetModel(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=128)
    label = models.CharField(max_length=255)
    asset_type = models.SmallIntegerField()
    fk_pays = models.IntegerField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat')
    fk_user_modif = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_modif', related_name='llxassetmodel_fk_user_modif_set', blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_asset_model'
        unique_together = (('entity', 'ref'),)


class LlxAssetModelExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_asset_model_extrafields'


class LlxAutoProcessor(models.Model):
    rowid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    batch_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_auto_processor'


class LlxBank(models.Model):
    rowid = models.AutoField(primary_key=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    datev = models.DateField(blank=True, null=True)
    dateo = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    amount_main_currency = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_rappro = models.IntegerField(blank=True, null=True)
    fk_type = models.CharField(max_length=6, blank=True, null=True)
    num_releve = models.CharField(max_length=50, blank=True, null=True)
    num_chq = models.CharField(max_length=50, blank=True, null=True)
    numero_compte = models.CharField(max_length=32, blank=True, null=True)
    rappro = models.SmallIntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    fk_bordereau = models.IntegerField(blank=True, null=True)
    banque = models.CharField(max_length=255, blank=True, null=True)
    emetteur = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=40, blank=True, null=True)
    origin_id = models.IntegerField(blank=True, null=True)
    origin_type = models.CharField(max_length=64, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_bank'


class LlxBankAccount(models.Model):
    rowid = models.AutoField(primary_key=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    ref = models.CharField(max_length=12)
    label = models.CharField(max_length=30)
    entity = models.IntegerField()
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    bank = models.CharField(max_length=60, blank=True, null=True)
    code_banque = models.CharField(max_length=128, blank=True, null=True)
    code_guichet = models.CharField(max_length=6, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    cle_rib = models.CharField(max_length=5, blank=True, null=True)
    bic = models.CharField(max_length=11, blank=True, null=True)
    iban_prefix = models.CharField(max_length=34, blank=True, null=True)
    country_iban = models.CharField(max_length=2, blank=True, null=True)
    cle_iban = models.CharField(max_length=2, blank=True, null=True)
    domiciliation = models.CharField(max_length=255, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    fk_pays = models.IntegerField()
    proprio = models.CharField(max_length=60, blank=True, null=True)
    owner_address = models.CharField(max_length=255, blank=True, null=True)
    courant = models.SmallIntegerField()
    clos = models.SmallIntegerField()
    rappro = models.SmallIntegerField(blank=True, null=True)
    url = models.CharField(max_length=128, blank=True, null=True)
    account_number = models.CharField(max_length=32, blank=True, null=True)
    fk_accountancy_journal = models.ForeignKey(LlxAccountingJournal, models.DO_NOTHING, db_column='fk_accountancy_journal', blank=True, null=True)
    currency_code = models.CharField(max_length=3)
    min_allowed = models.IntegerField(blank=True, null=True)
    min_desired = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    ics = models.CharField(max_length=32, blank=True, null=True)
    ics_transfer = models.CharField(max_length=32, blank=True, null=True)
    pti_in_ctti = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_bank_account'
        unique_together = (('label', 'entity'),)


class LlxBankAccountExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_bank_account_extrafields'


class LlxBankAccountHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField(blank=True, null=True)
    ref = models.CharField(max_length=12, blank=True, null=True)
    label = models.CharField(max_length=30, blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    bank = models.CharField(max_length=60, blank=True, null=True)
    code_banque = models.CharField(max_length=128, blank=True, null=True)
    code_guichet = models.CharField(max_length=6, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    cle_rib = models.CharField(max_length=5, blank=True, null=True)
    bic = models.CharField(max_length=11, blank=True, null=True)
    iban_prefix = models.CharField(max_length=34, blank=True, null=True)
    country_iban = models.CharField(max_length=2, blank=True, null=True)
    cle_iban = models.CharField(max_length=2, blank=True, null=True)
    domiciliation = models.CharField(max_length=255, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    fk_pays = models.IntegerField(blank=True, null=True)
    proprio = models.CharField(max_length=60, blank=True, null=True)
    owner_address = models.CharField(max_length=255, blank=True, null=True)
    courant = models.SmallIntegerField(blank=True, null=True)
    clos = models.SmallIntegerField(blank=True, null=True)
    rappro = models.SmallIntegerField(blank=True, null=True)
    url = models.CharField(max_length=128, blank=True, null=True)
    account_number = models.CharField(max_length=32, blank=True, null=True)
    fk_accountancy_journal = models.IntegerField(blank=True, null=True)
    currency_code = models.CharField(max_length=3, blank=True, null=True)
    min_allowed = models.IntegerField(blank=True, null=True)
    min_desired = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    ics = models.CharField(max_length=32, blank=True, null=True)
    ics_transfer = models.CharField(max_length=32, blank=True, null=True)
    operation_type = models.CharField(max_length=10, blank=True, null=True)
    operation_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_bank_account_history'


class LlxBankCateg(models.Model):
    rowid = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_bank_categ'


class LlxBankClass(models.Model):
    lineid = models.IntegerField()
    fk_categ = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_bank_class'
        unique_together = (('lineid', 'fk_categ'),)


class LlxBankUrl(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_bank = models.IntegerField(blank=True, null=True)
    url_id = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'llx_bank_url'
        unique_together = (('fk_bank', 'url_id', 'type'),)


class LlxBatch(models.Model):
    rowid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_date = models.DateField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_batch'


class LlxBatchCassetteCounts(models.Model):
    rowid = models.AutoField(primary_key=True)
    batch_details_cassettes = models.ForeignKey('LlxBatchDetailsCassettes', models.DO_NOTHING, db_column='batch_details_cassettes', blank=True, null=True)
    total_cassettes_count = models.IntegerField()
    created_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    batch = models.ForeignKey(LlxBatch, models.DO_NOTHING, db_column='batch', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_batch_cassette_counts'


class LlxBatchDetails(models.Model):
    rowid = models.AutoField(primary_key=True)
    batch_number = models.ForeignKey(LlxBatch, models.DO_NOTHING, db_column='batch_number', blank=True, null=True)
    lab_number = models.CharField(max_length=50)
    gross_station = models.CharField(max_length=50)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_batch_details'


class LlxBatchDetailsCassettes(models.Model):
    rowid = models.AutoField(primary_key=True)
    batch_details = models.ForeignKey(LlxBatchDetails, models.DO_NOTHING, db_column='batch_details', blank=True, null=True)
    cassettes_number = models.CharField(max_length=50)
    created_date = models.DateField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_batch_details_cassettes'


class LlxBlockedlog(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    action = models.CharField(max_length=50, blank=True, null=True)
    amounts = models.DecimalField(max_digits=24, decimal_places=8)
    element = models.CharField(max_length=50, blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    user_fullname = models.CharField(max_length=255, blank=True, null=True)
    fk_object = models.IntegerField(blank=True, null=True)
    ref_object = models.CharField(max_length=255, blank=True, null=True)
    date_object = models.DateTimeField(blank=True, null=True)
    signature = models.CharField(max_length=100)
    signature_line = models.CharField(max_length=100)
    object_data = models.TextField(blank=True, null=True)
    object_version = models.CharField(max_length=32, blank=True, null=True)
    certified = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_blockedlog'


class LlxBlockedlogAuthority(models.Model):
    rowid = models.AutoField(primary_key=True)
    blockchain = models.TextField()
    signature = models.CharField(max_length=100)
    tms = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_blockedlog_authority'


class LlxBomBom(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=128)
    bomtype = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    fk_warehouse = models.IntegerField(blank=True, null=True)
    qty = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    efficiency = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    duration = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat')
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_bom_bom'
        unique_together = (('ref', 'entity'),)


class LlxBomBomExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_bom_bom_extrafields'


class LlxBomBomline(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_bom = models.ForeignKey(LlxBomBom, models.DO_NOTHING, db_column='fk_bom')
    fk_product = models.IntegerField()
    fk_bom_child = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    qty = models.DecimalField(max_digits=24, decimal_places=8)
    qty_frozen = models.SmallIntegerField(blank=True, null=True)
    disable_stock_change = models.SmallIntegerField(blank=True, null=True)
    efficiency = models.DecimalField(max_digits=24, decimal_places=8)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_bom_bomline'


class LlxBomBomlineExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_bom_bomline_extrafields'


class LlxBone(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_gross_id = models.IntegerField()
    section_code = models.CharField(max_length=50, blank=True, null=True)
    tissue = models.CharField(max_length=100, blank=True, null=True)
    cassettes_number = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_bone'


class LlxBookmark(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_user = models.IntegerField()
    dateb = models.DateTimeField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    target = models.CharField(max_length=16, blank=True, null=True)
    title = models.CharField(max_length=64, blank=True, null=True)
    favicon = models.CharField(max_length=24, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    entity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_bookmark'
        unique_together = (('fk_user', 'entity', 'title'),)


class LlxBordereauCheque(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    date_bordereau = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    nbcheque = models.SmallIntegerField()
    fk_bank_account = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    statut = models.SmallIntegerField()
    tms = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    entity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_bordereau_cheque'
        unique_together = (('ref', 'entity'),)


class LlxBoxes(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    box = models.ForeignKey('LlxBoxesDef', models.DO_NOTHING)
    position = models.SmallIntegerField()
    box_order = models.CharField(max_length=3)
    fk_user = models.IntegerField()
    maxline = models.IntegerField(blank=True, null=True)
    params = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_boxes'
        unique_together = (('entity', 'box', 'position', 'fk_user'),)


class LlxBoxesDef(models.Model):
    rowid = models.AutoField(primary_key=True)
    file = models.CharField(max_length=200)
    entity = models.IntegerField()
    tms = models.DateTimeField()
    note = models.CharField(max_length=130, blank=True, null=True)
    fk_user = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_boxes_def'
        unique_together = (('file', 'entity', 'note'),)


class LlxBudget(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    label = models.CharField(max_length=255)
    status = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_budget'


class LlxBudgetLines(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_budget = models.ForeignKey(LlxBudget, models.DO_NOTHING, db_column='fk_budget')
    fk_project_ids = models.CharField(max_length=180)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_budget_lines'
        unique_together = (('fk_budget', 'fk_project_ids'),)


class LlxCAccountingCategory(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    code = models.CharField(max_length=16)
    label = models.CharField(max_length=255)
    range_account = models.CharField(max_length=255)
    sens = models.SmallIntegerField()
    category_type = models.SmallIntegerField()
    formula = models.CharField(max_length=255)
    position = models.IntegerField(blank=True, null=True)
    fk_country = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_accounting_category'
        unique_together = (('code', 'entity'),)


class LlxCActionTrigger(models.Model):
    rowid = models.AutoField(primary_key=True)
    elementtype = models.CharField(max_length=64)
    code = models.CharField(unique=True, max_length=64)
    label = models.CharField(max_length=128)
    description = models.CharField(max_length=255, blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_action_trigger'


class LlxCActioncomm(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=50)
    type = models.CharField(max_length=50)
    libelle = models.CharField(max_length=128)
    module = models.CharField(max_length=50, blank=True, null=True)
    active = models.SmallIntegerField()
    todo = models.SmallIntegerField(blank=True, null=True)
    color = models.CharField(max_length=9, blank=True, null=True)
    picto = models.CharField(max_length=48, blank=True, null=True)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_actioncomm'


class LlxCAssetDisposalType(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    code = models.CharField(max_length=16)
    label = models.CharField(max_length=50)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_asset_disposal_type'
        unique_together = (('code', 'entity'),)


class LlxCAvailability(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=30)
    label = models.CharField(max_length=128)
    active = models.SmallIntegerField()
    position = models.IntegerField()
    type_duration = models.CharField(max_length=1, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_availability'


class LlxCBarcodeType(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16)
    entity = models.IntegerField()
    libelle = models.CharField(max_length=128)
    coder = models.CharField(max_length=16)
    example = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'llx_c_barcode_type'
        unique_together = (('code', 'entity'),)


class LlxCChargesociales(models.Model):
    libelle = models.CharField(max_length=128, blank=True, null=True)
    deductible = models.SmallIntegerField()
    active = models.SmallIntegerField()
    code = models.CharField(max_length=12)
    accountancy_code = models.CharField(max_length=32, blank=True, null=True)
    fk_pays = models.IntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_chargesociales'


class LlxCCivility(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=6)
    label = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_civility'


class LlxCCountry(models.Model):
    rowid = models.IntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=2)
    code_iso = models.CharField(unique=True, max_length=3, blank=True, null=True)
    label = models.CharField(unique=True, max_length=128)
    eec = models.SmallIntegerField(blank=True, null=True)
    active = models.SmallIntegerField()
    favorite = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_country'


class LlxCCurrencies(models.Model):
    code_iso = models.CharField(primary_key=True, max_length=3)
    label = models.CharField(max_length=128)
    unicode = models.CharField(max_length=32, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_currencies'


class LlxCDepartements(models.Model):
    rowid = models.AutoField(primary_key=True)
    code_departement = models.CharField(max_length=6)
    fk_region = models.ForeignKey('LlxCRegions', models.DO_NOTHING, db_column='fk_region', to_field='code_region', blank=True, null=True)
    cheflieu = models.CharField(max_length=50, blank=True, null=True)
    tncc = models.IntegerField(blank=True, null=True)
    ncc = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_departements'
        unique_together = (('code_departement', 'fk_region'),)


class LlxCEcotaxe(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=64)
    label = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    fk_pays = models.IntegerField()
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_ecotaxe'


class LlxCEffectif(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=12)
    libelle = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_effectif'


class LlxCEmailSenderprofile(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    private = models.SmallIntegerField()
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    label = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    signature = models.TextField(blank=True, null=True)
    position = models.SmallIntegerField(blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_email_senderprofile'
        unique_together = (('entity', 'label', 'email'),)


class LlxCEmailTemplates(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)
    type_template = models.CharField(max_length=32, blank=True, null=True)
    lang = models.CharField(max_length=6, blank=True, null=True)
    private = models.SmallIntegerField()
    fk_user = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    label = models.CharField(max_length=180, blank=True, null=True)
    position = models.SmallIntegerField(blank=True, null=True)
    enabled = models.CharField(max_length=255, blank=True, null=True)
    active = models.SmallIntegerField()
    topic = models.TextField(blank=True, null=True)
    joinfiles = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    content_lines = models.TextField(blank=True, null=True)
    email_from = models.CharField(max_length=255, blank=True, null=True)
    email_to = models.CharField(max_length=255, blank=True, null=True)
    email_tocc = models.CharField(max_length=255, blank=True, null=True)
    email_tobcc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_email_templates'
        unique_together = (('entity', 'label', 'lang'),)


class LlxCExpTaxCat(models.Model):
    rowid = models.AutoField(primary_key=True)
    label = models.CharField(max_length=128)
    entity = models.IntegerField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_exp_tax_cat'


class LlxCExpTaxRange(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_c_exp_tax_cat = models.IntegerField()
    range_ik = models.DecimalField(max_digits=65535, decimal_places=65535)
    entity = models.IntegerField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_exp_tax_range'


class LlxCFieldList(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    element = models.CharField(max_length=64)
    entity = models.IntegerField()
    name = models.CharField(max_length=32)
    alias = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    align = models.CharField(max_length=6, blank=True, null=True)
    sort = models.SmallIntegerField()
    search = models.SmallIntegerField()
    visible = models.SmallIntegerField()
    enabled = models.CharField(max_length=255, blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_field_list'


class LlxCFormatCards(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    paper_size = models.CharField(max_length=20)
    orientation = models.CharField(max_length=1)
    metric = models.CharField(max_length=5)
    leftmargin = models.DecimalField(max_digits=24, decimal_places=8)
    topmargin = models.DecimalField(max_digits=24, decimal_places=8)
    nx = models.IntegerField()
    ny = models.IntegerField()
    spacex = models.DecimalField(max_digits=24, decimal_places=8)
    spacey = models.DecimalField(max_digits=24, decimal_places=8)
    width = models.DecimalField(max_digits=24, decimal_places=8)
    height = models.DecimalField(max_digits=24, decimal_places=8)
    font_size = models.IntegerField()
    custom_x = models.DecimalField(max_digits=24, decimal_places=8)
    custom_y = models.DecimalField(max_digits=24, decimal_places=8)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_format_cards'


class LlxCFormeJuridique(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.IntegerField(unique=True)
    fk_pays = models.IntegerField()
    libelle = models.CharField(max_length=255, blank=True, null=True)
    isvatexempted = models.SmallIntegerField()
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_forme_juridique'


class LlxCHolidayTypes(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=16)
    label = models.CharField(max_length=255)
    affect = models.IntegerField()
    delay = models.IntegerField()
    newbymonth = models.DecimalField(max_digits=8, decimal_places=5)
    fk_country = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    block_if_negative = models.IntegerField()
    sortorder = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_holiday_types'


class LlxCHrmDepartment(models.Model):
    rowid = models.IntegerField(primary_key=True)
    pos = models.SmallIntegerField()
    code = models.CharField(max_length=16)
    label = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_hrm_department'


class LlxCHrmFunction(models.Model):
    rowid = models.IntegerField(primary_key=True)
    pos = models.SmallIntegerField()
    code = models.CharField(max_length=16)
    label = models.CharField(max_length=128, blank=True, null=True)
    c_level = models.SmallIntegerField()
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_hrm_function'


class LlxCHrmPublicHoliday(models.Model):
    entity = models.IntegerField()
    fk_country = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=62, blank=True, null=True)
    dayrule = models.CharField(max_length=64, blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_hrm_public_holiday'
        unique_together = (('entity', 'code'), ('entity', 'fk_country', 'dayrule', 'day', 'month', 'year'),)


class LlxCIncoterms(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=3)
    label = models.CharField(max_length=100, blank=True, null=True)
    libelle = models.CharField(max_length=255)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_incoterms'


class LlxCInputMethod(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=30, blank=True, null=True)
    libelle = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_input_method'


class LlxCInputReason(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=30, blank=True, null=True)
    label = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_input_reason'


class LlxCLeadStatus(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=10, blank=True, null=True)
    label = models.CharField(max_length=128, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_lead_status'


class LlxCPaiement(models.Model):
    entity = models.IntegerField()
    code = models.CharField(max_length=6)
    libelle = models.CharField(max_length=62, blank=True, null=True)
    type = models.SmallIntegerField(blank=True, null=True)
    active = models.SmallIntegerField()
    accountancy_code = models.CharField(max_length=32, blank=True, null=True)
    module = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_paiement'
        unique_together = (('entity', 'code'),)


class LlxCPaiementHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    id = models.IntegerField(blank=True, null=True)
    entity = models.IntegerField()
    code = models.CharField(max_length=6, blank=True, null=True)
    libelle = models.CharField(max_length=62, blank=True, null=True)
    type = models.SmallIntegerField(blank=True, null=True)
    active = models.SmallIntegerField()
    accountancy_code = models.CharField(max_length=32, blank=True, null=True)
    module = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField()
    operation_type = models.CharField(max_length=10, blank=True, null=True)
    operation_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_paiement_history'


class LlxCPaperFormat(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16)
    label = models.CharField(max_length=128)
    width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=5)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_paper_format'


class LlxCPartnershipType(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    code = models.CharField(max_length=32)
    label = models.CharField(max_length=128)
    active = models.SmallIntegerField()
    keyword = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_partnership_type'
        unique_together = (('entity', 'code'),)


class LlxCPaymentTerm(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    code = models.CharField(max_length=16, blank=True, null=True)
    sortorder = models.SmallIntegerField(blank=True, null=True)
    active = models.SmallIntegerField(blank=True, null=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    libelle_facture = models.TextField(blank=True, null=True)
    type_cdr = models.SmallIntegerField(blank=True, null=True)
    nbjour = models.SmallIntegerField(blank=True, null=True)
    decalage = models.SmallIntegerField(blank=True, null=True)
    module = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField()
    deposit_percent = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_payment_term'
        unique_together = (('entity', 'code'),)


class LlxCPaymentTermHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField()
    entity = models.IntegerField()
    code = models.CharField(max_length=16, blank=True, null=True)
    sortorder = models.SmallIntegerField(blank=True, null=True)
    active = models.SmallIntegerField(blank=True, null=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    libelle_facture = models.TextField(blank=True, null=True)
    type_cdr = models.SmallIntegerField(blank=True, null=True)
    nbjour = models.SmallIntegerField(blank=True, null=True)
    decalage = models.SmallIntegerField(blank=True, null=True)
    module = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField()
    operation_type = models.CharField(max_length=10, blank=True, null=True)
    operation_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_payment_term_history'


class LlxCPriceExpression(models.Model):
    rowid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    expression = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'llx_c_price_expression'


class LlxCPriceGlobalVariable(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    value = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_price_global_variable'


class LlxCPriceGlobalVariableUpdater(models.Model):
    rowid = models.AutoField(primary_key=True)
    type = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    parameters = models.TextField(blank=True, null=True)
    fk_variable = models.IntegerField()
    update_interval = models.IntegerField(blank=True, null=True)
    next_update = models.IntegerField(blank=True, null=True)
    last_status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_price_global_variable_updater'


class LlxCProductNature(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.SmallIntegerField(unique=True)
    label = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_product_nature'


class LlxCProductbatchQcstatus(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    code = models.CharField(max_length=16)
    label = models.CharField(max_length=128)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_productbatch_qcstatus'
        unique_together = (('code', 'entity'),)


class LlxCPropalst(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=12)
    label = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_propalst'


class LlxCProspectcontactlevel(models.Model):
    code = models.CharField(primary_key=True, max_length=12)
    label = models.CharField(max_length=128, blank=True, null=True)
    sortorder = models.SmallIntegerField(blank=True, null=True)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_prospectcontactlevel'


class LlxCProspectlevel(models.Model):
    code = models.CharField(primary_key=True, max_length=12)
    label = models.CharField(max_length=128, blank=True, null=True)
    sortorder = models.SmallIntegerField(blank=True, null=True)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_prospectlevel'


class LlxCRecruitmentOrigin(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=32)
    label = models.CharField(max_length=128)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_recruitment_origin'


class LlxCRegions(models.Model):
    rowid = models.AutoField(primary_key=True)
    code_region = models.IntegerField(unique=True)
    fk_pays = models.ForeignKey(LlxCCountry, models.DO_NOTHING, db_column='fk_pays')
    cheflieu = models.CharField(max_length=50, blank=True, null=True)
    tncc = models.IntegerField(blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_regions'


class LlxCRevenuestamp(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_pays = models.IntegerField()
    taux = models.DecimalField(max_digits=65535, decimal_places=65535)
    revenuestamp_type = models.CharField(max_length=16)
    note = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()
    accountancy_code_sell = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_revenuestamp'


class LlxCShipmentMode(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    tms = models.DateTimeField()
    code = models.CharField(max_length=30)
    libelle = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    tracking = models.CharField(max_length=255, blank=True, null=True)
    active = models.SmallIntegerField(blank=True, null=True)
    module = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_shipment_mode'
        unique_together = (('code', 'entity'),)


class LlxCShipmentPackageType(models.Model):
    rowid = models.AutoField(primary_key=True)
    label = models.CharField(max_length=128)
    description = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField()
    entity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_shipment_package_type'


class LlxCSocialnetworks(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    code = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=150, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=20, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_socialnetworks'
        unique_together = (('entity', 'code'),)


class LlxCStcomm(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=24)
    libelle = models.CharField(max_length=128, blank=True, null=True)
    picto = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_stcomm'


class LlxCStcommcontact(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=12)
    libelle = models.CharField(max_length=128, blank=True, null=True)
    picto = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_stcommcontact'


class LlxCTicketCategory(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=32)
    label = models.CharField(max_length=128)
    public = models.IntegerField(blank=True, null=True)
    use_default = models.IntegerField(blank=True, null=True)
    fk_parent = models.IntegerField()
    force_severity = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    pos = models.IntegerField()
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_ticket_category'
        unique_together = (('code', 'entity'),)


class LlxCTicketResolution(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=32)
    pos = models.CharField(max_length=32)
    label = models.CharField(max_length=128)
    active = models.IntegerField(blank=True, null=True)
    use_default = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_ticket_resolution'


class LlxCTicketSeverity(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=32)
    pos = models.CharField(max_length=32)
    label = models.CharField(max_length=128)
    color = models.CharField(max_length=10, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    use_default = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_ticket_severity'


class LlxCTicketType(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=32)
    pos = models.CharField(max_length=32)
    label = models.CharField(max_length=128)
    active = models.IntegerField(blank=True, null=True)
    use_default = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_ticket_type'


class LlxCTransportMode(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    code = models.CharField(max_length=3)
    label = models.CharField(max_length=255)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_transport_mode'
        unique_together = (('code', 'entity'),)


class LlxCTva(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_pays = models.IntegerField()
    code = models.CharField(max_length=10, blank=True, null=True)
    taux = models.DecimalField(max_digits=65535, decimal_places=65535)
    localtax1 = models.CharField(max_length=20)
    localtax1_type = models.CharField(max_length=10)
    localtax2 = models.CharField(max_length=20)
    localtax2_type = models.CharField(max_length=10)
    recuperableonly = models.IntegerField()
    note = models.CharField(max_length=128, blank=True, null=True)
    active = models.SmallIntegerField()
    accountancy_code_sell = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_c_tva'
        unique_together = (('fk_pays', 'code', 'taux', 'recuperableonly'),)


class LlxCTypeContact(models.Model):
    rowid = models.IntegerField(primary_key=True)
    element = models.CharField(max_length=30)
    source = models.CharField(max_length=8)
    code = models.CharField(max_length=32)
    libelle = models.CharField(max_length=128)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_type_contact'
        unique_together = (('element', 'source', 'code'),)


class LlxCTypeContainer(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=32)
    entity = models.IntegerField()
    label = models.CharField(max_length=128)
    module = models.CharField(max_length=32, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_type_container'
        unique_together = (('code', 'entity'),)


class LlxCTypeFees(models.Model):
    code = models.CharField(unique=True, max_length=12)
    label = models.CharField(max_length=128, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    accountancy_code = models.CharField(max_length=32, blank=True, null=True)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_type_fees'


class LlxCTypeResource(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=32)
    label = models.CharField(max_length=128)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_type_resource'
        unique_together = (('label', 'code'),)


class LlxCTypent(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=12)
    libelle = models.CharField(max_length=128, blank=True, null=True)
    fk_country = models.IntegerField(blank=True, null=True)
    active = models.SmallIntegerField()
    module = models.CharField(max_length=32, blank=True, null=True)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_typent'


class LlxCUnits(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=3, blank=True, null=True)
    sortorder = models.SmallIntegerField(blank=True, null=True)
    scale = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=128, blank=True, null=True)
    short_label = models.CharField(max_length=5, blank=True, null=True)
    unit_type = models.CharField(max_length=10, blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_units'


class LlxCZiptown(models.Model):
    rowid = models.AutoField(primary_key=True)
    code = models.CharField(max_length=5, blank=True, null=True)
    fk_county = models.ForeignKey(LlxCDepartements, models.DO_NOTHING, db_column='fk_county', blank=True, null=True)
    fk_pays = models.ForeignKey(LlxCCountry, models.DO_NOTHING, db_column='fk_pays')
    zip = models.CharField(max_length=10)
    town = models.CharField(max_length=180)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_c_ziptown'
        unique_together = (('zip', 'town', 'fk_pays'),)


class LlxCategorie(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    fk_parent = models.IntegerField()
    label = models.CharField(max_length=180)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=8, blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    visible = models.SmallIntegerField()
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie'


class LlxCategorieAccount(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_account')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_account = models.ForeignKey(LlxBankAccount, models.DO_NOTHING, db_column='fk_account')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_account'
        unique_together = (('fk_categorie', 'fk_account'),)


class LlxCategorieActioncomm(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_actioncomm')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_actioncomm = models.ForeignKey(LlxActioncomm, models.DO_NOTHING, db_column='fk_actioncomm')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_actioncomm'
        unique_together = (('fk_categorie', 'fk_actioncomm'),)


class LlxCategorieContact(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_socpeople')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_socpeople = models.ForeignKey('LlxSocpeople', models.DO_NOTHING, db_column='fk_socpeople')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_contact'
        unique_together = (('fk_categorie', 'fk_socpeople'),)


class LlxCategorieFournisseur(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_soc')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_fournisseur'
        unique_together = (('fk_categorie', 'fk_soc'),)


class LlxCategorieKnowledgemanagement(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_knowledgemanagement')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_knowledgemanagement = models.ForeignKey('LlxKnowledgemanagementKnowledgerecord', models.DO_NOTHING, db_column='fk_knowledgemanagement')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_knowledgemanagement'
        unique_together = (('fk_categorie', 'fk_knowledgemanagement'),)


class LlxCategorieLang(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_category = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_category')
    lang = models.CharField(max_length=5)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_lang'
        unique_together = (('fk_category', 'lang'),)


class LlxCategorieMember(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_member')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_member = models.ForeignKey(LlxAdherent, models.DO_NOTHING, db_column='fk_member')

    class Meta:
        managed = False
        db_table = 'llx_categorie_member'
        unique_together = (('fk_categorie', 'fk_member'),)


class LlxCategorieProduct(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_product')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_product = models.ForeignKey('LlxProduct', models.DO_NOTHING, db_column='fk_product')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_product'
        unique_together = (('fk_categorie', 'fk_product'),)


class LlxCategorieProject(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_project')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_project = models.ForeignKey('LlxProjet', models.DO_NOTHING, db_column='fk_project')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_project'
        unique_together = (('fk_categorie', 'fk_project'),)


class LlxCategorieSociete(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_soc')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_societe'
        unique_together = (('fk_categorie', 'fk_soc'),)


class LlxCategorieTicket(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_ticket')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_ticket = models.ForeignKey('LlxTicket', models.DO_NOTHING, db_column='fk_ticket')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_ticket'
        unique_together = (('fk_categorie', 'fk_ticket'),)


class LlxCategorieUser(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_user')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_user = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_user'
        unique_together = (('fk_categorie', 'fk_user'),)


class LlxCategorieWarehouse(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_warehouse')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_warehouse = models.ForeignKey('LlxEntrepot', models.DO_NOTHING, db_column='fk_warehouse')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_warehouse'
        unique_together = (('fk_categorie', 'fk_warehouse'),)


class LlxCategorieWebsitePage(models.Model):
    pk = models.CompositePrimaryKey('fk_categorie', 'fk_website_page')
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_website_page = models.ForeignKey('LlxWebsitePage', models.DO_NOTHING, db_column='fk_website_page')
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categorie_website_page'
        unique_together = (('fk_categorie', 'fk_website_page'),)


class LlxCategoriesExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_categories_extrafields'


class LlxChargesociales(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=16, blank=True, null=True)
    date_ech = models.DateTimeField(blank=True, null=True)
    libelle = models.CharField(max_length=80)
    entity = models.IntegerField()
    tms = models.DateTimeField()
    date_creation = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_type = models.IntegerField()
    fk_account = models.IntegerField(blank=True, null=True)
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    paye = models.SmallIntegerField()
    periode = models.DateField(blank=True, null=True)
    fk_projet = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_chargesociales'


class LlxClinicalDetails(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    clinical_details = models.CharField(max_length=1000, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_clinical_details'


class LlxClinicalDetailsHistory(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    clinical_details = models.CharField(max_length=2000, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_clinical_details_history'


class LlxCommande(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_int = models.CharField(max_length=255, blank=True, null=True)
    ref_client = models.CharField(max_length=255, blank=True, null=True)
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    fk_projet = models.ForeignKey('LlxProjet', models.DO_NOTHING, db_column='fk_projet', blank=True, null=True)
    tms = models.DateTimeField()
    date_creation = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    date_cloture = models.DateTimeField(blank=True, null=True)
    date_commande = models.DateField(blank=True, null=True)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_valid', related_name='llxcommande_fk_user_valid_set', blank=True, null=True)
    fk_user_cloture = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_cloture', related_name='llxcommande_fk_user_cloture_set', blank=True, null=True)
    source = models.SmallIntegerField(blank=True, null=True)
    fk_statut = models.SmallIntegerField(blank=True, null=True)
    amount_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise_absolue = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    module_source = models.CharField(max_length=32, blank=True, null=True)
    pos_source = models.CharField(max_length=32, blank=True, null=True)
    facture = models.SmallIntegerField(blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_currency = models.CharField(max_length=3, blank=True, null=True)
    fk_cond_reglement = models.IntegerField(blank=True, null=True)
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    date_livraison = models.DateTimeField(blank=True, null=True)
    fk_shipping_method = models.IntegerField(blank=True, null=True)
    fk_warehouse = models.IntegerField(blank=True, null=True)
    fk_availability = models.IntegerField(blank=True, null=True)
    fk_input_reason = models.IntegerField(blank=True, null=True)
    fk_delivery_address = models.IntegerField(blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    deposit_percent = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande'
        unique_together = (('ref', 'entity'),)


class LlxCommandeExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)
    test_type = models.CharField(max_length=255, blank=True, null=True)
    test_code = models.CharField(max_length=255, blank=True, null=True)
    prev_fnac = models.CharField(max_length=255, blank=True, null=True)
    prev_biopsy_date = models.DateField(blank=True, null=True)
    prev_biopsy_op = models.CharField(max_length=255, blank=True, null=True)
    informed = models.CharField(max_length=255, blank=True, null=True)
    given = models.CharField(max_length=255, blank=True, null=True)
    referredby_dr = models.CharField(max_length=255, blank=True, null=True)
    referred_from = models.CharField(max_length=255, blank=True, null=True)
    add_history = models.CharField(max_length=255, blank=True, null=True)
    other_labno = models.CharField(max_length=255, blank=True, null=True)
    referred_by_dr = models.CharField(max_length=255, blank=True, null=True)
    referredfrom = models.CharField(max_length=255, blank=True, null=True)
    aikl_dr = models.CharField(max_length=255, blank=True, null=True)
    courier = models.CharField(max_length=255, blank=True, null=True)
    num_containers = models.CharField(max_length=255, blank=True, null=True)
    prev_biopsy = models.CharField(max_length=255, blank=True, null=True)
    prev_fnac_date = models.DateField(blank=True, null=True)
    prev_fnac_op = models.CharField(max_length=255, blank=True, null=True)
    referred_by_dr2 = models.CharField(max_length=255, blank=True, null=True)
    referred_by_dr_text = models.CharField(max_length=255, blank=True, null=True)
    referredfrom_text = models.CharField(max_length=255, blank=True, null=True)
    invno = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_extrafields'


class LlxCommandeExtrafieldsHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField(blank=True, null=True)
    fk_object = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    test_type = models.CharField(max_length=255, blank=True, null=True)
    test_code = models.CharField(max_length=255, blank=True, null=True)
    prev_fnac = models.CharField(max_length=255, blank=True, null=True)
    prev_biopsy_date = models.DateField(blank=True, null=True)
    prev_biopsy_op = models.CharField(max_length=255, blank=True, null=True)
    informed = models.CharField(max_length=255, blank=True, null=True)
    given = models.CharField(max_length=255, blank=True, null=True)
    referredby_dr = models.CharField(max_length=255, blank=True, null=True)
    referred_from = models.CharField(max_length=255, blank=True, null=True)
    add_history = models.CharField(max_length=255, blank=True, null=True)
    other_labno = models.CharField(max_length=255, blank=True, null=True)
    referred_by_dr = models.CharField(max_length=255, blank=True, null=True)
    referredfrom = models.CharField(max_length=255, blank=True, null=True)
    aikl_dr = models.CharField(max_length=255, blank=True, null=True)
    courier = models.CharField(max_length=255, blank=True, null=True)
    num_containers = models.CharField(max_length=255, blank=True, null=True)
    prev_biopsy = models.CharField(max_length=255, blank=True, null=True)
    prev_fnac_date = models.DateField(blank=True, null=True)
    prev_fnac_op = models.CharField(max_length=255, blank=True, null=True)
    referred_by_dr2 = models.CharField(max_length=255, blank=True, null=True)
    referred_by_dr_text = models.CharField(max_length=255, blank=True, null=True)
    referredfrom_text = models.CharField(max_length=255, blank=True, null=True)
    invno = models.CharField(max_length=255, blank=True, null=True)
    operation = models.CharField(max_length=10)
    operation_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_commande_extrafields_history'


class LlxCommandeFournisseur(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=180)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_supplier = models.CharField(max_length=255, blank=True, null=True)
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    fk_projet = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField()
    date_creation = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    date_approve = models.DateTimeField(blank=True, null=True)
    date_approve2 = models.DateTimeField(blank=True, null=True)
    date_commande = models.DateField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_user_approve = models.IntegerField(blank=True, null=True)
    fk_user_approve2 = models.IntegerField(blank=True, null=True)
    source = models.SmallIntegerField()
    fk_statut = models.SmallIntegerField(blank=True, null=True)
    billed = models.SmallIntegerField(blank=True, null=True)
    amount_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    date_livraison = models.DateTimeField(blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_cond_reglement = models.IntegerField(blank=True, null=True)
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    fk_input_method = models.IntegerField(blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_fournisseur'
        unique_together = (('ref', 'fk_soc', 'entity'),)


class LlxCommandeFournisseurDispatch(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_commande = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    fk_commandefourndet = models.IntegerField(blank=True, null=True)
    fk_projet = models.IntegerField(blank=True, null=True)
    fk_reception = models.ForeignKey('LlxReception', models.DO_NOTHING, db_column='fk_reception', blank=True, null=True)
    qty = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fk_entrepot = models.IntegerField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    batch = models.CharField(max_length=128, blank=True, null=True)
    eatby = models.DateField(blank=True, null=True)
    sellby = models.DateField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    cost_price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_fournisseur_dispatch'


class LlxCommandeFournisseurDispatchExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_fournisseur_dispatch_extrafields'


class LlxCommandeFournisseurExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_fournisseur_extrafields'


class LlxCommandeFournisseurLog(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    datelog = models.DateTimeField(blank=True, null=True)
    fk_commande = models.IntegerField()
    fk_statut = models.SmallIntegerField()
    fk_user = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_fournisseur_log'


class LlxCommandeFournisseurdet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_commande = models.IntegerField()
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=50, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_fournisseurdet'


class LlxCommandeFournisseurdetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_fournisseurdet_extrafields'


class LlxCommandeGrossdr(models.Model):
    create_time = models.DateTimeField(blank=True, null=True)
    labno = models.CharField(max_length=12, blank=True, null=True)
    soc_dr = models.ForeignKey('LlxUser', models.DO_NOTHING, blank=True, null=True)
    fk_track = models.ForeignKey('LlxCommandeTrackws', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_grossdr'
        db_table_comment = 'Worksheet Assignment Tracking Table'


class LlxCommandeHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=30, blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_int = models.CharField(max_length=255, blank=True, null=True)
    ref_client = models.CharField(max_length=255, blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_projet = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    date_cloture = models.DateTimeField(blank=True, null=True)
    date_commande = models.DateField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_user_cloture = models.IntegerField(blank=True, null=True)
    source = models.SmallIntegerField(blank=True, null=True)
    fk_statut = models.SmallIntegerField(blank=True, null=True)
    amount_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise_absolue = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    module_source = models.CharField(max_length=32, blank=True, null=True)
    pos_source = models.CharField(max_length=32, blank=True, null=True)
    facture = models.SmallIntegerField(blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_currency = models.CharField(max_length=3, blank=True, null=True)
    fk_cond_reglement = models.IntegerField(blank=True, null=True)
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    date_livraison = models.DateTimeField(blank=True, null=True)
    fk_shipping_method = models.IntegerField(blank=True, null=True)
    fk_warehouse = models.IntegerField(blank=True, null=True)
    fk_availability = models.IntegerField(blank=True, null=True)
    fk_input_reason = models.IntegerField(blank=True, null=True)
    fk_delivery_address = models.IntegerField(blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    operation = models.CharField(max_length=10, blank=True, null=True)
    operation_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_history'


class LlxCommandeTrackws(models.Model):
    create_time = models.DateTimeField(blank=True, null=True, db_comment='Time when status was added')
    labno = models.CharField(max_length=12, blank=True, null=True, db_comment='Lab Number of Worksheet')
    user_id = models.IntegerField(blank=True, null=True, db_comment='User who added status')
    fk_status = models.ForeignKey('LlxCommandeWsstatus', models.DO_NOTHING, blank=True, null=True, db_comment='ID of current status')
    description = models.CharField(max_length=20000, blank=True, null=True)
    lab_room_status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commande_trackws'
        db_table_comment = 'Worksheet Status Tracking Table'


class LlxCommandeWsstatus(models.Model):
    create_time = models.DateTimeField(blank=True, null=True, db_comment='Time Status was created')
    name = models.CharField(max_length=255, blank=True, null=True, db_comment='Name of Status')
    process_order = models.IntegerField(blank=True, null=True, db_comment='Order of Status in Process')
    section = models.CharField(max_length=255, blank=True, null=True, db_comment='Section where Status is applicable')
    optional = models.BooleanField(blank=True, null=True, db_comment='Is status optional in worksheet process flow. True means optional')

    class Meta:
        managed = False
        db_table = 'llx_commande_wsstatus'
        db_table_comment = 'List of Status for Worksheets'


class LlxCommandedet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_commande = models.ForeignKey(LlxCommande, models.DO_NOTHING, db_column='fk_commande')
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    buy_price_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_product_fournisseur_price = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    fk_commandefourndet = models.ForeignKey(LlxCommandeFournisseurdet, models.DO_NOTHING, db_column='fk_commandefourndet', blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commandedet'


class LlxCommandedetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)
    sample_serial = models.CharField(max_length=255, blank=True, null=True)
    fixative_changed = models.CharField(max_length=255, blank=True, null=True)
    fixative = models.CharField(max_length=255, blank=True, null=True)
    container = models.CharField(max_length=255, blank=True, null=True)
    container_label = models.CharField(max_length=255, blank=True, null=True)
    op_date = models.DateTimeField(blank=True, null=True)
    left_right = models.CharField(max_length=255, blank=True, null=True)
    sample_details = models.TextField(blank=True, null=True)
    slide_count = models.CharField(max_length=255, blank=True, null=True)
    slide_stain = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commandedet_extrafields'


class LlxCommandedetExtrafieldsHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField(blank=True, null=True)
    fk_object = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    sample_serial = models.CharField(max_length=255, blank=True, null=True)
    fixative_changed = models.CharField(max_length=255, blank=True, null=True)
    fixative = models.CharField(max_length=255, blank=True, null=True)
    container = models.CharField(max_length=255, blank=True, null=True)
    container_label = models.CharField(max_length=255, blank=True, null=True)
    op_date = models.DateTimeField(blank=True, null=True)
    left_right = models.CharField(max_length=255, blank=True, null=True)
    sample_details = models.TextField(blank=True, null=True)
    slide_count = models.CharField(max_length=255, blank=True, null=True)
    slide_stain = models.CharField(max_length=255, blank=True, null=True)
    operation = models.CharField(max_length=10, blank=True, null=True)
    operation_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commandedet_extrafields_history'


class LlxCommandedetHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField(blank=True, null=True)
    fk_commande = models.IntegerField(blank=True, null=True)
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    buy_price_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_product_fournisseur_price = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    fk_unit = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    fk_commandefourndet = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    operation = models.CharField(max_length=10)
    operation_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_commandedet_history'


class LlxComment(models.Model):
    rowid = models.AutoField(primary_key=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    description = models.TextField()
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_element = models.IntegerField(blank=True, null=True)
    element_type = models.CharField(max_length=50, blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=125, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_comment'


class LlxConst(models.Model):
    rowid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=180)
    entity = models.IntegerField()
    value = models.TextField()
    type = models.CharField(max_length=64, blank=True, null=True)
    visible = models.SmallIntegerField()
    note = models.TextField(blank=True, null=True)
    tms = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_const'
        unique_together = (('name', 'entity'),)


class LlxContrat(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=255, blank=True, null=True)
    ref_customer = models.CharField(max_length=255, blank=True, null=True)
    ref_supplier = models.CharField(max_length=255, blank=True, null=True)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField()
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    date_contrat = models.DateTimeField(blank=True, null=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    fin_validite = models.DateTimeField(blank=True, null=True)
    date_cloture = models.DateTimeField(blank=True, null=True)
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    fk_projet = models.IntegerField(blank=True, null=True)
    fk_commercial_signature = models.IntegerField(blank=True, null=True)
    fk_commercial_suivi = models.IntegerField(blank=True, null=True)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author')
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_cloture = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_contrat'
        unique_together = (('ref', 'entity'),)


class LlxContratExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_contrat_extrafields'


class LlxContratdet(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_contrat = models.ForeignKey(LlxContrat, models.DO_NOTHING, db_column='fk_contrat')
    fk_product = models.ForeignKey('LlxProduct', models.DO_NOTHING, db_column='fk_product', blank=True, null=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    date_commande = models.DateTimeField(blank=True, null=True)
    date_ouverture_prevue = models.DateTimeField(blank=True, null=True)
    date_ouverture = models.DateTimeField(blank=True, null=True)
    date_fin_validite = models.DateTimeField(blank=True, null=True)
    date_cloture = models.DateTimeField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    qty = models.FloatField()
    remise_percent = models.FloatField(blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_ht = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    buy_price_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_product_fournisseur_price = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField()
    fk_user_ouverture = models.IntegerField(blank=True, null=True)
    fk_user_cloture = models.IntegerField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_contratdet'


class LlxContratdetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_contratdet_extrafields'


class LlxContratdetLog(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_contratdet = models.ForeignKey(LlxContratdet, models.DO_NOTHING, db_column='fk_contratdet')
    date = models.DateTimeField(blank=True, null=True)
    statut = models.SmallIntegerField()
    fk_user_author = models.IntegerField()
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_contratdet_log'


class LlxCronjob(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    jobtype = models.CharField(max_length=10)
    label = models.CharField(max_length=255)
    command = models.CharField(max_length=255, blank=True, null=True)
    classesname = models.CharField(max_length=255, blank=True, null=True)
    objectname = models.CharField(max_length=255, blank=True, null=True)
    methodename = models.CharField(max_length=255, blank=True, null=True)
    params = models.TextField(blank=True, null=True)
    md5params = models.CharField(max_length=32, blank=True, null=True)
    module_name = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    datelastrun = models.DateTimeField(blank=True, null=True)
    datenextrun = models.DateTimeField(blank=True, null=True)
    datestart = models.DateTimeField(blank=True, null=True)
    dateend = models.DateTimeField(blank=True, null=True)
    datelastresult = models.DateTimeField(blank=True, null=True)
    lastresult = models.TextField(blank=True, null=True)
    lastoutput = models.TextField(blank=True, null=True)
    unitfrequency = models.CharField(max_length=255)
    frequency = models.IntegerField()
    maxrun = models.IntegerField()
    nbrun = models.IntegerField(blank=True, null=True)
    autodelete = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    processing = models.IntegerField()
    test = models.CharField(max_length=255, blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_mod = models.IntegerField(blank=True, null=True)
    fk_mailing = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    libname = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    email_alert = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cronjob'
        unique_together = (('label', 'entity'),)


class LlxCustomTrigger(models.Model):
    rowid = models.AutoField(primary_key=True)
    trigger_value = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_custom_trigger'


class LlxCyto(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50)
    patient_code = models.CharField(max_length=50, blank=True, null=True)
    fna_station_type = models.CharField(max_length=50, blank=True, null=True)
    doctor = models.CharField(max_length=50, blank=True, null=True)
    assistant = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto'


class LlxCytoClinicalInformation(models.Model):
    rowid = models.AutoField(primary_key=True)
    cyto_id = models.CharField(max_length=50, blank=True, null=True)
    chief_complain = models.TextField(blank=True, null=True)
    relevant_clinical_history = models.TextField(blank=True, null=True)
    on_examination = models.TextField(blank=True, null=True)
    clinical_impression = models.TextField(blank=True, null=True)
    previous_chief_complain = models.JSONField(blank=True, null=True)
    previous_history = models.JSONField(blank=True, null=True)
    previous_on_examination = models.JSONField(blank=True, null=True)
    previous_clinical_impression = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_clinical_information'


class LlxCytoDoctorCaseInfo(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50)
    screening = models.BooleanField(blank=True, null=True)
    screening_datetime = models.DateTimeField(blank=True, null=True)
    screening_count = models.CharField(max_length=20, blank=True, null=True)
    screening_count_data = models.JSONField(blank=True, null=True)
    finalization = models.BooleanField(blank=True, null=True)
    finalization_datetime = models.DateTimeField(blank=True, null=True)
    finalization_count_data = models.JSONField(blank=True, null=True)
    screening_doctor_name = models.CharField(max_length=50, blank=True, null=True)
    finalization_doctor_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_doctor_case_info'


class LlxCytoDoctorCompleteCase(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50)
    screening_done = models.BooleanField(blank=True, null=True)
    screening_done_date_time = models.DateTimeField(blank=True, null=True)
    screening_done_count = models.CharField(max_length=50, blank=True, null=True)
    screening_done_count_data = models.JSONField(blank=True, null=True)
    finalization_done = models.BooleanField(blank=True, null=True)
    finalization_done_date_time = models.DateTimeField(blank=True, null=True)
    finalization_done_count = models.CharField(max_length=50, blank=True, null=True)
    finalization_done_count_data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_doctor_complete_case'


class LlxCytoDoctorDiagnosis(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    previous_diagnosis = models.TextField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_doctor_diagnosis'


class LlxCytoDoctorLabInstruction(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50)
    screening_stain_name = models.CharField(max_length=255, blank=True, null=True)
    screening_doctor_name = models.CharField(max_length=255, blank=True, null=True)
    screening_stain_again = models.JSONField(blank=True, null=True)
    finalization_stain_name = models.CharField(max_length=5000, blank=True, null=True)
    finalization_doctor_name = models.CharField(max_length=50, blank=True, null=True)
    finalization_stain_again = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_doctor_lab_instruction'


class LlxCytoDoctorStudyPatientInfo(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50)
    screening_study = models.BooleanField(blank=True, null=True)
    screening_patient_history = models.JSONField(blank=True, null=True)
    screening_study_count = models.CharField(max_length=20, blank=True, null=True)
    screening_study_count_data = models.JSONField(blank=True, null=True)
    finalization_study = models.BooleanField(blank=True, null=True)
    finalization_patient_history = models.JSONField(blank=True, null=True)
    screening_doctor_name = models.CharField(max_length=50, blank=True, null=True)
    finalization_doctor_name = models.CharField(max_length=50, blank=True, null=True)
    finalization_study_count = models.CharField(max_length=20, blank=True, null=True)
    finalization_study_count_data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_doctor_study_patient_info'


class LlxCytoFixationAdditionalDetails(models.Model):
    rowid = models.AutoField(primary_key=True)
    cyto_id = models.CharField(max_length=50, blank=True, null=True)
    dry_slides_description = models.TextField(blank=True, null=True)
    additional_notes_on_fixation = models.TextField(blank=True, null=True)
    special_instructions_or_tests_required = models.TextField(blank=True, null=True)
    number_of_needle_used = models.CharField(max_length=50, blank=True, null=True)
    number_of_syringe_used = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_fixation_additional_details'


class LlxCytoFixationDetails(models.Model):
    rowid = models.AutoField(primary_key=True)
    cyto_id = models.CharField(max_length=50, blank=True, null=True)
    slide_number = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    fixation_method = models.CharField(max_length=500, blank=True, null=True)
    dry = models.CharField(max_length=20, blank=True, null=True)
    aspiration_materials = models.TextField(blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_fixation_details'


class LlxCytoLabInstructionStatus(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(unique=True, max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    status_list = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_lab_instruction_status'


class LlxCytoMicroscopicDescription(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50)
    microscopic_description = models.TextField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    aspiration_notes = models.TextField(blank=True, null=True)
    gross_note = models.TextField(blank=True, null=True)
    recall = models.TextField(blank=True, null=True)
    chief_complain = models.TextField(blank=True, null=True)
    specimen_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_microscopic_description'


class LlxCytoRecall(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    patient_code = models.CharField(max_length=50, blank=True, null=True)
    fna_station_type = models.CharField(max_length=50, blank=True, null=True)
    doctor = models.CharField(max_length=50, blank=True, null=True)
    assistant = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_recall'


class LlxCytoRecallClinicalInformation(models.Model):
    rowid = models.AutoField(primary_key=True)
    cyto_id = models.CharField(max_length=50)
    chief_complain = models.TextField(blank=True, null=True)
    additional_relevant_clinical_history = models.TextField(blank=True, null=True)
    additional_findings_on_examination = models.TextField(blank=True, null=True)
    additional_clinical_impression = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_recall_clinical_information'


class LlxCytoRecallFixationAdditionalDetails(models.Model):
    rowid = models.AutoField(primary_key=True)
    cyto_id = models.CharField(max_length=50)
    dry_slides_description = models.TextField(blank=True, null=True)
    additional_notes_on_fixation = models.TextField(blank=True, null=True)
    number_of_needle_used = models.CharField(max_length=50, blank=True, null=True)
    number_of_syringe_used = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_recall_fixation_additional_details'


class LlxCytoRecallFixationDetails(models.Model):
    rowid = models.AutoField(primary_key=True)
    cyto_id = models.CharField(max_length=50)
    slide_number = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    fixation_method = models.CharField(max_length=500, blank=True, null=True)
    dry = models.CharField(max_length=20, blank=True, null=True)
    aspiration_materials = models.TextField(blank=True, null=True)
    special_instructions = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_recall_fixation_details'


class LlxCytoRecallManagement(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=20, blank=True, null=True)
    patient_code = models.CharField(max_length=20, blank=True, null=True)
    recall_reason = models.JSONField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    recalled_doctor = models.CharField(max_length=50, blank=True, null=True)
    notified_user = models.CharField(max_length=50, blank=True, null=True)
    notified_method = models.TextField(blank=True, null=True)
    follow_up_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_recall_management'


class LlxCytoReportDelivered(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=20, blank=True, null=True)
    patient_code = models.CharField(max_length=20, blank=True, null=True)
    report_type = models.CharField(max_length=100, blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    delivered_user = models.CharField(max_length=50, blank=True, null=True)
    delivered_method = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    delivered_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_report_delivered'
        db_table_comment = 'This table tracks data where patient additional reports like MRI, CT scan, or other reports that need to be viewed in microscopy to see the slide.'


class LlxCytoReportReceived(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=20, blank=True, null=True)
    patient_code = models.CharField(max_length=20, blank=True, null=True)
    report_type = models.CharField(max_length=100, blank=True, null=True)
    received_date = models.DateTimeField(blank=True, null=True)
    received_user = models.CharField(max_length=50, blank=True, null=True)
    received_method = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    received_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_report_received'


class LlxCytoReportRequest(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=20, blank=True, null=True)
    patient_code = models.CharField(max_length=20, blank=True, null=True)
    report_type = models.CharField(max_length=100, blank=True, null=True)
    request_date = models.DateTimeField(blank=True, null=True)
    doctor = models.CharField(max_length=50, blank=True, null=True)
    notified_user = models.CharField(max_length=50, blank=True, null=True)
    notified_method = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    request_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_report_request'


class LlxCytoSlideCentrifuge(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    slide_number = models.TextField(blank=True, null=True)
    pipette_tips = models.TextField(blank=True, null=True)
    filter_paper = models.TextField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_slide_centrifuge'


class LlxCytoSlidePrepared(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_slide_prepared'


class LlxCytoSpecialInstructionsComplete(models.Model):
    rowid = models.AutoField(primary_key=True)
    fixation_details = models.ForeignKey(LlxCytoFixationDetails, models.DO_NOTHING, db_column='fixation_details', blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_special_instructions_complete'


class LlxCytoStudyPatientInfoDispatchCenter(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    status_list = models.JSONField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_cyto_study_patient_info_dispatch_center'


class LlxDefaultValues(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    type = models.CharField(max_length=10, blank=True, null=True)
    user_id = models.IntegerField()
    page = models.CharField(max_length=255, blank=True, null=True)
    param = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_default_values'
        unique_together = (('type', 'entity', 'user_id', 'page', 'param'),)


class LlxDelivery(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_int = models.CharField(max_length=255, blank=True, null=True)
    ref_customer = models.CharField(max_length=255, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    fk_user_valid = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_valid', related_name='llxdelivery_fk_user_valid_set', blank=True, null=True)
    date_delivery = models.DateTimeField(blank=True, null=True)
    fk_address = models.IntegerField(blank=True, null=True)
    fk_statut = models.SmallIntegerField(blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_delivery'
        unique_together = (('ref', 'entity'),)


class LlxDeliveryExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_delivery_extrafields'


class LlxDeliverydet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_delivery = models.ForeignKey(LlxDelivery, models.DO_NOTHING, db_column='fk_delivery', blank=True, null=True)
    fk_origin_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_deliverydet'


class LlxDeliverydetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_deliverydet_extrafields'


class LlxDeplacement(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30, blank=True, null=True)
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    dated = models.DateTimeField(blank=True, null=True)
    fk_user = models.IntegerField()
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=12)
    fk_statut = models.IntegerField()
    km = models.FloatField(blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_projet = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_deplacement'


class LlxDiagnosis(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    specimen = models.CharField(max_length=550, blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_diagnosis'


class LlxDiagnosisHistory(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    specimen = models.CharField(max_length=550, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_diagnosis_history'


class LlxDoctorAssistedBySignature(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    doctor_username = models.CharField(max_length=500, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_doctor_assisted_by_signature'


class LlxDoctorDegination(models.Model):
    row_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_doctor_degination'


class LlxDoctorDeginationHistory(models.Model):
    row_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_doctor_degination_history'


class LlxDoctorFinalizedBySignature(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    doctor_username = models.CharField(max_length=500, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_doctor_finalized_by_signature'


class LlxDoctorsContact(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=128)
    label = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_project = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat')
    fk_user_modif = models.IntegerField(blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_doctors_contact'


class LlxDoctorsContactExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_doctors_contact_extrafields'


class LlxDocumentModel(models.Model):
    rowid = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    entity = models.IntegerField()
    type = models.CharField(max_length=64)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_document_model'
        unique_together = (('nom', 'type', 'entity'),)


class LlxDon(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30, blank=True, null=True)
    entity = models.IntegerField()
    tms = models.DateTimeField()
    fk_statut = models.SmallIntegerField()
    datedon = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_payment = models.IntegerField(blank=True, null=True)
    paid = models.SmallIntegerField()
    fk_soc = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    societe = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip = models.CharField(max_length=30, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    fk_country = models.IntegerField()
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=24, blank=True, null=True)
    phone_mobile = models.CharField(max_length=24, blank=True, null=True)
    public = models.SmallIntegerField()
    fk_projet = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_don'


class LlxDonExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_don_extrafields'


class LlxDuplicateReportDoctorAssisted(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    doctor_username = models.CharField(max_length=100, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    previous_signature = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_duplicate_report_doctor_assisted'


class LlxDuplicateReportDoctorFinalizedBySignature(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    doctor_username = models.CharField(max_length=100, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    previous_signature = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_duplicate_report_doctor_finalized_by_signature'


class LlxEcmDirectories(models.Model):
    rowid = models.AutoField(primary_key=True)
    label = models.CharField(max_length=64)
    entity = models.IntegerField()
    fk_parent = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255)
    cachenbofdoc = models.IntegerField()
    fullpath = models.CharField(max_length=750, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    date_c = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_c = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_c', blank=True, null=True)
    fk_user_m = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_m', related_name='llxecmdirectories_fk_user_m_set', blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    acl = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_ecm_directories'
        unique_together = (('label', 'fk_parent', 'entity'),)


class LlxEcmDirectoriesExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_ecm_directories_extrafields'


class LlxEcmFiles(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=128, blank=True, null=True)
    label = models.CharField(max_length=128)
    share = models.CharField(max_length=128, blank=True, null=True)
    entity = models.IntegerField()
    filepath = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    src_object_type = models.CharField(max_length=64, blank=True, null=True)
    src_object_id = models.IntegerField(blank=True, null=True)
    fullpath_orig = models.CharField(max_length=750, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=750, blank=True, null=True)
    cover = models.TextField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    gen_or_uploaded = models.CharField(max_length=12, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    date_c = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_c = models.IntegerField(blank=True, null=True)
    fk_user_m = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    acl = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_ecm_files'
        unique_together = (('filepath', 'filename', 'entity'),)


class LlxEcmFilesExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_ecm_files_extrafields'


class LlxElementContact(models.Model):
    rowid = models.AutoField(primary_key=True)
    datecreate = models.DateTimeField(blank=True, null=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    element_id = models.IntegerField()
    fk_c_type_contact = models.ForeignKey(LlxCTypeContact, models.DO_NOTHING, db_column='fk_c_type_contact')
    fk_socpeople = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_element_contact'
        unique_together = (('element_id', 'fk_c_type_contact', 'fk_socpeople'),)


class LlxElementElement(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_source = models.IntegerField()
    sourcetype = models.CharField(max_length=32)
    fk_target = models.IntegerField()
    targettype = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'llx_element_element'
        unique_together = (('fk_source', 'sourcetype', 'fk_target', 'targettype'),)


class LlxElementElementHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField()
    fk_source = models.IntegerField()
    sourcetype = models.CharField(max_length=32)
    fk_target = models.IntegerField()
    targettype = models.CharField(max_length=32)
    operation_type = models.CharField(max_length=10, blank=True, null=True)
    operation_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_element_element_history'


class LlxElementResources(models.Model):
    rowid = models.AutoField(primary_key=True)
    element_id = models.IntegerField(blank=True, null=True)
    element_type = models.CharField(max_length=64, blank=True, null=True)
    resource_id = models.IntegerField(blank=True, null=True)
    resource_type = models.CharField(max_length=64, blank=True, null=True)
    busy = models.IntegerField(blank=True, null=True)
    mandatory = models.IntegerField(blank=True, null=True)
    duree = models.FloatField(blank=True, null=True)
    fk_user_create = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_element_resources'
        unique_together = (('resource_id', 'resource_type', 'element_id', 'element_type'),)


class LlxElementTag(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_categorie = models.ForeignKey(LlxCategorie, models.DO_NOTHING, db_column='fk_categorie')
    fk_element = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_element_tag'
        unique_together = (('fk_categorie', 'fk_element'),)


class LlxEmailcollectorEmailcollector(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=128)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    host = models.CharField(max_length=255, blank=True, null=True)
    hostcharset = models.CharField(max_length=16, blank=True, null=True)
    login = models.CharField(max_length=128, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    source_directory = models.CharField(max_length=255)
    target_directory = models.CharField(max_length=255, blank=True, null=True)
    maxemailpercollect = models.IntegerField(blank=True, null=True)
    datelastresult = models.DateTimeField(blank=True, null=True)
    codelastresult = models.CharField(max_length=16, blank=True, null=True)
    lastresult = models.CharField(max_length=255, blank=True, null=True)
    datelastok = models.DateTimeField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    status = models.IntegerField()
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_emailcollector_emailcollector'
        unique_together = (('ref', 'entity'),)


class LlxEmailcollectorEmailcollectoraction(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_emailcollector = models.ForeignKey(LlxEmailcollectorEmailcollector, models.DO_NOTHING, db_column='fk_emailcollector')
    type = models.CharField(max_length=128)
    actionparam = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_emailcollector_emailcollectoraction'
        unique_together = (('fk_emailcollector', 'type'),)


class LlxEmailcollectorEmailcollectorfilter(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_emailcollector = models.ForeignKey(LlxEmailcollectorEmailcollector, models.DO_NOTHING, db_column='fk_emailcollector')
    type = models.CharField(max_length=128)
    rulevalue = models.CharField(max_length=128, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_emailcollector_emailcollectorfilter'
        unique_together = (('fk_emailcollector', 'type', 'rulevalue'),)


class LlxEntrepot(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=255)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    entity = models.IntegerField()
    fk_project = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lieu = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    fk_departement = models.IntegerField(blank=True, null=True)
    fk_pays = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    warehouse_usage = models.IntegerField(blank=True, null=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    fk_parent = models.IntegerField(blank=True, null=True)
    barcode = models.CharField(max_length=180, blank=True, null=True)
    fk_barcode_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_entrepot'
        unique_together = (('ref', 'entity'),)


class LlxEntrepotExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_entrepot_extrafields'


class LlxEstablishment(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=25, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    fk_state = models.IntegerField(blank=True, null=True)
    fk_country = models.IntegerField(blank=True, null=True)
    profid1 = models.CharField(max_length=20, blank=True, null=True)
    profid2 = models.CharField(max_length=20, blank=True, null=True)
    profid3 = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fk_user_author = models.IntegerField()
    fk_user_mod = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    status = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_establishment'


class LlxEventElement(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_source = models.IntegerField()
    fk_target = models.IntegerField()
    targettype = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'llx_event_element'


class LlxEventorganizationConferenceorboothattendee(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=128)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_actioncomm = models.IntegerField(blank=True, null=True)
    fk_project = models.IntegerField()
    fk_invoice = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    date_subscription = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    email_company = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_eventorganization_conferenceorboothattendee'
        unique_together = (('fk_project', 'email', 'fk_actioncomm'),)


class LlxEventorganizationConferenceorboothattendeeExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_eventorganization_conferenceorboothattendee_extrafields'


class LlxEvents(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    type = models.CharField(max_length=32)
    entity = models.IntegerField()
    prefix_session = models.CharField(max_length=255, blank=True, null=True)
    dateevent = models.DateTimeField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=250)
    ip = models.CharField(max_length=250)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    fk_object = models.IntegerField(blank=True, null=True)
    authentication_method = models.CharField(max_length=64, blank=True, null=True)
    fk_oauth_token = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_events'


class LlxExpedition(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    fk_projet = models.IntegerField(blank=True, null=True)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_int = models.CharField(max_length=255, blank=True, null=True)
    ref_customer = models.CharField(max_length=255, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    fk_user_valid = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_valid', related_name='llxexpedition_fk_user_valid_set', blank=True, null=True)
    date_delivery = models.DateTimeField(blank=True, null=True)
    date_expedition = models.DateTimeField(blank=True, null=True)
    fk_address = models.IntegerField(blank=True, null=True)
    fk_shipping_method = models.ForeignKey(LlxCShipmentMode, models.DO_NOTHING, db_column='fk_shipping_method', blank=True, null=True)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    fk_statut = models.SmallIntegerField(blank=True, null=True)
    billed = models.SmallIntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    width = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    size_units = models.IntegerField(blank=True, null=True)
    size = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    weight_units = models.IntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expedition'
        unique_together = (('ref', 'entity'),)


class LlxExpeditionExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expedition_extrafields'


class LlxExpeditionPackage(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_expedition = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    value = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_package_type = models.IntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    width = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    size = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    size_units = models.IntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    weight_units = models.IntegerField(blank=True, null=True)
    dangerous_goods = models.SmallIntegerField(blank=True, null=True)
    tail_lift = models.SmallIntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expedition_package'


class LlxExpeditiondet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_expedition = models.ForeignKey(LlxExpedition, models.DO_NOTHING, db_column='fk_expedition')
    fk_origin_line = models.IntegerField(blank=True, null=True)
    fk_entrepot = models.IntegerField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expeditiondet'


class LlxExpeditiondetBatch(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_expeditiondet = models.ForeignKey(LlxExpeditiondet, models.DO_NOTHING, db_column='fk_expeditiondet')
    eatby = models.DateField(blank=True, null=True)
    sellby = models.DateField(blank=True, null=True)
    batch = models.CharField(max_length=128, blank=True, null=True)
    qty = models.DecimalField(max_digits=65535, decimal_places=65535)
    fk_origin_stock = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_expeditiondet_batch'


class LlxExpeditiondetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expeditiondet_extrafields'


class LlxExpensereport(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=50)
    entity = models.IntegerField()
    ref_number_int = models.IntegerField(blank=True, null=True)
    ref_ext = models.IntegerField(blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    date_create = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    date_approve = models.DateTimeField(blank=True, null=True)
    date_refuse = models.DateTimeField(blank=True, null=True)
    date_cancel = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_author = models.IntegerField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_user_validator = models.IntegerField(blank=True, null=True)
    fk_user_approve = models.IntegerField(blank=True, null=True)
    fk_user_refuse = models.IntegerField(blank=True, null=True)
    fk_user_cancel = models.IntegerField(blank=True, null=True)
    fk_statut = models.IntegerField()
    fk_c_paiement = models.IntegerField(blank=True, null=True)
    paid = models.SmallIntegerField()
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    detail_refuse = models.CharField(max_length=255, blank=True, null=True)
    detail_cancel = models.CharField(max_length=255, blank=True, null=True)
    integration_compta = models.IntegerField(blank=True, null=True)
    fk_bank_account = models.IntegerField(blank=True, null=True)
    model_pdf = models.CharField(max_length=50, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expensereport'
        unique_together = (('ref', 'entity'),)


class LlxExpensereportDet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_expensereport = models.IntegerField()
    docnumber = models.CharField(max_length=128, blank=True, null=True)
    fk_c_type_fees = models.IntegerField()
    fk_c_exp_tax_cat = models.IntegerField(blank=True, null=True)
    fk_projet = models.IntegerField(blank=True, null=True)
    comments = models.TextField()
    product_type = models.IntegerField(blank=True, null=True)
    qty = models.FloatField()
    subprice = models.DecimalField(max_digits=24, decimal_places=8)
    value_unit = models.DecimalField(max_digits=24, decimal_places=8)
    remise_percent = models.FloatField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8)
    date = models.DateField()
    info_bits = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_facture = models.IntegerField(blank=True, null=True)
    fk_ecm_files = models.IntegerField(blank=True, null=True)
    fk_code_ventilation = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    rule_warning_message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expensereport_det'


class LlxExpensereportExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expensereport_extrafields'


class LlxExpensereportIk(models.Model):
    rowid = models.AutoField(primary_key=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_c_exp_tax_cat = models.IntegerField()
    fk_range = models.IntegerField()
    coef = models.DecimalField(max_digits=65535, decimal_places=65535)
    ikoffset = models.DecimalField(max_digits=65535, decimal_places=65535)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expensereport_ik'


class LlxExpensereportRules(models.Model):
    rowid = models.AutoField(primary_key=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    dates = models.DateTimeField(blank=True, null=True)
    datee = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    restrictive = models.SmallIntegerField()
    fk_user = models.IntegerField(blank=True, null=True)
    fk_usergroup = models.IntegerField(blank=True, null=True)
    fk_c_type_fees = models.IntegerField()
    code_expense_rules_type = models.CharField(max_length=50)
    is_for_all = models.SmallIntegerField(blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_expensereport_rules'


class LlxExportCompta(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=12)
    date_export = models.DateTimeField(blank=True, null=True)
    fk_user = models.IntegerField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_export_compta'


class LlxExportModel(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField(blank=True, null=True)
    fk_user = models.IntegerField()
    label = models.CharField(max_length=50)
    type = models.CharField(max_length=64)
    field = models.TextField()
    filter = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_export_model'
        unique_together = (('label', 'type'),)


class LlxExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    entity = models.IntegerField()
    elementtype = models.CharField(max_length=64)
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=8, blank=True, null=True)
    size = models.CharField(max_length=8, blank=True, null=True)
    fieldcomputed = models.TextField(blank=True, null=True)
    fielddefault = models.CharField(max_length=255, blank=True, null=True)
    fieldunique = models.IntegerField(blank=True, null=True)
    fieldrequired = models.IntegerField(blank=True, null=True)
    perms = models.CharField(max_length=255, blank=True, null=True)
    enabled = models.CharField(max_length=255, blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)
    alwayseditable = models.IntegerField(blank=True, null=True)
    param = models.TextField(blank=True, null=True)
    list = models.CharField(max_length=255, blank=True, null=True)
    printable = models.IntegerField(blank=True, null=True)
    totalizable = models.BooleanField(blank=True, null=True)
    langs = models.CharField(max_length=64, blank=True, null=True)
    help = models.TextField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    css = models.CharField(max_length=128, blank=True, null=True)
    cssview = models.CharField(max_length=128, blank=True, null=True)
    csslist = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_extrafields'
        unique_together = (('name', 'entity', 'elementtype'),)


class LlxFacture(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_int = models.CharField(max_length=255, blank=True, null=True)
    ref_client = models.CharField(max_length=255, blank=True, null=True)
    type = models.SmallIntegerField()
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    datec = models.DateTimeField(blank=True, null=True)
    datef = models.DateField(blank=True, null=True)
    date_pointoftax = models.DateField(blank=True, null=True)
    date_valid = models.DateField(blank=True, null=True)
    tms = models.DateTimeField()
    date_closing = models.DateTimeField(blank=True, null=True)
    paye = models.SmallIntegerField()
    remise_percent = models.FloatField(blank=True, null=True)
    remise_absolue = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    close_code = models.CharField(max_length=16, blank=True, null=True)
    close_note = models.CharField(max_length=128, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    revenuestamp = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_statut = models.SmallIntegerField()
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_valid', related_name='llxfacture_fk_user_valid_set', blank=True, null=True)
    fk_user_closing = models.IntegerField(blank=True, null=True)
    module_source = models.CharField(max_length=32, blank=True, null=True)
    pos_source = models.CharField(max_length=32, blank=True, null=True)
    fk_fac_rec_source = models.IntegerField(blank=True, null=True)
    fk_facture_source = models.ForeignKey('self', models.DO_NOTHING, db_column='fk_facture_source', blank=True, null=True)
    fk_projet = models.ForeignKey('LlxProjet', models.DO_NOTHING, db_column='fk_projet', blank=True, null=True)
    increment = models.CharField(max_length=10, blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_currency = models.CharField(max_length=3, blank=True, null=True)
    fk_cond_reglement = models.IntegerField()
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    date_lim_reglement = models.DateField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    fk_transport_mode = models.IntegerField(blank=True, null=True)
    situation_cycle_ref = models.SmallIntegerField(blank=True, null=True)
    situation_counter = models.SmallIntegerField(blank=True, null=True)
    situation_final = models.SmallIntegerField(blank=True, null=True)
    retained_warranty = models.FloatField(blank=True, null=True)
    retained_warranty_date_limit = models.DateField(blank=True, null=True)
    retained_warranty_fk_cond_reglement = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture'
        unique_together = (('ref', 'entity'),)


class LlxFactureExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)
    payments_all = models.CharField(max_length=255, blank=True, null=True)
    date_delivery = models.CharField(max_length=255, blank=True, null=True)
    drname_qual = models.CharField(max_length=255, blank=True, null=True)
    hosname = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    word_total_ttc = models.CharField(max_length=255, blank=True, null=True)
    labno = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_extrafields'


class LlxFactureFourn(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=180)
    ref_supplier = models.CharField(max_length=180)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    type = models.SmallIntegerField()
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    datec = models.DateTimeField(blank=True, null=True)
    datef = models.DateField(blank=True, null=True)
    date_pointoftax = models.DateField(blank=True, null=True)
    date_valid = models.DateField(blank=True, null=True)
    tms = models.DateTimeField()
    date_closing = models.DateTimeField(blank=True, null=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    paye = models.SmallIntegerField()
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    remise = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    close_code = models.CharField(max_length=16, blank=True, null=True)
    close_note = models.CharField(max_length=128, blank=True, null=True)
    tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_statut = models.SmallIntegerField()
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_valid', related_name='llxfacturefourn_fk_user_valid_set', blank=True, null=True)
    fk_user_closing = models.IntegerField(blank=True, null=True)
    fk_facture_source = models.IntegerField(blank=True, null=True)
    fk_projet = models.ForeignKey('LlxProjet', models.DO_NOTHING, db_column='fk_projet', blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_cond_reglement = models.IntegerField(blank=True, null=True)
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    date_lim_reglement = models.DateField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    fk_transport_mode = models.IntegerField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_fac_rec_source = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_fourn'
        unique_together = (('ref', 'entity'), ('ref_supplier', 'fk_soc', 'entity'),)


class LlxFactureFournDet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_facture_fourn = models.ForeignKey(LlxFactureFourn, models.DO_NOTHING, db_column='fk_facture_fourn')
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=50, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pu_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    pu_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    fk_code_ventilation = models.IntegerField()
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_fourn_det'
        unique_together = (('fk_remise_except', 'fk_facture_fourn'),)


class LlxFactureFournDetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_fourn_det_extrafields'


class LlxFactureFournDetRec(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_facture_fourn = models.IntegerField()
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=50, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pu_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    pu_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.IntegerField(blank=True, null=True)
    date_end = models.IntegerField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_fourn_det_rec'


class LlxFactureFournDetRecExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_fourn_det_rec_extrafields'


class LlxFactureFournExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_fourn_extrafields'


class LlxFactureFournRec(models.Model):
    rowid = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    ref_supplier = models.CharField(max_length=180)
    entity = models.IntegerField()
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    suspended = models.IntegerField(blank=True, null=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    remise = models.FloatField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_projet = models.ForeignKey('LlxProjet', models.DO_NOTHING, db_column='fk_projet', blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_cond_reglement = models.IntegerField(blank=True, null=True)
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    date_lim_reglement = models.DateField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    modelpdf = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    usenewprice = models.IntegerField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    unit_frequency = models.CharField(max_length=2, blank=True, null=True)
    date_when = models.DateTimeField(blank=True, null=True)
    date_last_gen = models.DateTimeField(blank=True, null=True)
    nb_gen_done = models.IntegerField(blank=True, null=True)
    nb_gen_max = models.IntegerField(blank=True, null=True)
    auto_validate = models.IntegerField(blank=True, null=True)
    generate_pdf = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_fourn_rec'
        unique_together = (('titre', 'entity'), ('ref_supplier', 'fk_soc', 'entity'),)


class LlxFactureFournRecExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_fourn_rec_extrafields'


class LlxFactureHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField()
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_int = models.CharField(max_length=255, blank=True, null=True)
    ref_client = models.CharField(max_length=255, blank=True, null=True)
    type = models.SmallIntegerField()
    fk_soc = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    datef = models.DateField(blank=True, null=True)
    date_pointoftax = models.DateField(blank=True, null=True)
    date_valid = models.DateField(blank=True, null=True)
    tms = models.DateTimeField()
    date_closing = models.DateTimeField(blank=True, null=True)
    paye = models.SmallIntegerField()
    remise_percent = models.FloatField(blank=True, null=True)
    remise_absolue = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    close_code = models.CharField(max_length=16, blank=True, null=True)
    close_note = models.CharField(max_length=128, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    revenuestamp = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_statut = models.SmallIntegerField()
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_user_closing = models.IntegerField(blank=True, null=True)
    module_source = models.CharField(max_length=32, blank=True, null=True)
    pos_source = models.CharField(max_length=32, blank=True, null=True)
    fk_fac_rec_source = models.IntegerField(blank=True, null=True)
    fk_facture_source = models.IntegerField(blank=True, null=True)
    fk_projet = models.IntegerField(blank=True, null=True)
    increment = models.CharField(max_length=10, blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_currency = models.CharField(max_length=3, blank=True, null=True)
    fk_cond_reglement = models.IntegerField()
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    date_lim_reglement = models.DateField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    fk_transport_mode = models.IntegerField(blank=True, null=True)
    situation_cycle_ref = models.SmallIntegerField(blank=True, null=True)
    situation_counter = models.SmallIntegerField(blank=True, null=True)
    situation_final = models.SmallIntegerField(blank=True, null=True)
    retained_warranty = models.FloatField(blank=True, null=True)
    retained_warranty_date_limit = models.DateField(blank=True, null=True)
    retained_warranty_fk_cond_reglement = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    operation = models.CharField(max_length=10)
    operation_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_facture_history'


class LlxFactureRec(models.Model):
    rowid = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    entity = models.IntegerField()
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    suspended = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    remise = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise_absolue = models.FloatField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    revenuestamp = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_projet = models.ForeignKey('LlxProjet', models.DO_NOTHING, db_column='fk_projet', blank=True, null=True)
    fk_cond_reglement = models.IntegerField()
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    date_lim_reglement = models.DateField(blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    modelpdf = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    usenewprice = models.IntegerField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    unit_frequency = models.CharField(max_length=2, blank=True, null=True)
    date_when = models.DateTimeField(blank=True, null=True)
    date_last_gen = models.DateTimeField(blank=True, null=True)
    nb_gen_done = models.IntegerField(blank=True, null=True)
    nb_gen_max = models.IntegerField(blank=True, null=True)
    auto_validate = models.IntegerField(blank=True, null=True)
    generate_pdf = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_rec'
        unique_together = (('titre', 'entity'),)


class LlxFactureRecExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facture_rec_extrafields'


class LlxFacturedet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_facture = models.ForeignKey(LlxFacture, models.DO_NOTHING, db_column='fk_facture')
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    buy_price_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_product_fournisseur_price = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    fk_contract_line = models.IntegerField(blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    fk_code_ventilation = models.IntegerField()
    situation_percent = models.FloatField(blank=True, null=True)
    fk_prev_id = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facturedet'


class LlxFacturedetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facturedet_extrafields'


class LlxFacturedetHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField(blank=True, null=True)
    fk_facture = models.IntegerField(blank=True, null=True)
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    buy_price_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_product_fournisseur_price = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    fk_contract_line = models.IntegerField(blank=True, null=True)
    fk_unit = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    fk_code_ventilation = models.IntegerField(blank=True, null=True)
    situation_percent = models.FloatField(blank=True, null=True)
    fk_prev_id = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    operation_type = models.CharField(max_length=10, blank=True, null=True)
    operation_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facturedet_history'


class LlxFacturedetRec(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_facture = models.IntegerField()
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    date_start_fill = models.IntegerField(blank=True, null=True)
    date_end_fill = models.IntegerField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    buy_price_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_product_fournisseur_price = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    fk_contract_line = models.IntegerField(blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facturedet_rec'


class LlxFacturedetRecExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_facturedet_rec_extrafields'


class LlxFichinter(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    fk_projet = models.IntegerField(blank=True, null=True)
    fk_contrat = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=30)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField()
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    datei = models.DateField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_statut = models.SmallIntegerField(blank=True, null=True)
    dateo = models.DateField(blank=True, null=True)
    datee = models.DateField(blank=True, null=True)
    datet = models.DateField(blank=True, null=True)
    duree = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    ref_client = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_fichinter'
        unique_together = (('ref', 'entity'),)


class LlxFichinterExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_fichinter_extrafields'


class LlxFichinterRec(models.Model):
    rowid = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=50)
    entity = models.IntegerField()
    fk_soc = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    fk_contrat = models.IntegerField(blank=True, null=True)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    fk_projet = models.ForeignKey('LlxProjet', models.DO_NOTHING, db_column='fk_projet', blank=True, null=True)
    duree = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    modelpdf = models.CharField(max_length=50, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    unit_frequency = models.CharField(max_length=2, blank=True, null=True)
    date_when = models.DateTimeField(blank=True, null=True)
    date_last_gen = models.DateTimeField(blank=True, null=True)
    nb_gen_done = models.IntegerField(blank=True, null=True)
    nb_gen_max = models.IntegerField(blank=True, null=True)
    auto_validate = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_fichinter_rec'
        unique_together = (('titre', 'entity'),)


class LlxFichinterdet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_fichinter = models.ForeignKey(LlxFichinter, models.DO_NOTHING, db_column='fk_fichinter', blank=True, null=True)
    fk_parent_line = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duree = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_fichinterdet'


class LlxFichinterdetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_fichinterdet_extrafields'


class LlxFichinterdetRec(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_fichinter = models.IntegerField()
    date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duree = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    localtax1_type = models.CharField(max_length=1, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    localtax2_type = models.CharField(max_length=1, blank=True, null=True)
    qty = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remise_percent = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remise = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    buy_price_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_product_fournisseur_price = models.IntegerField(blank=True, null=True)
    fk_code_ventilation = models.IntegerField()
    fk_export_commpta = models.IntegerField()
    special_code = models.IntegerField(blank=True, null=True)
    fk_unit = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_fichinterdet_rec'


class LlxGross(models.Model):
    gross_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=255, blank=True, null=True)
    patient_code = models.CharField(max_length=255, blank=True, null=True)
    gross_station_type = models.CharField(max_length=50, blank=True, null=True)
    gross_assistant_name = models.CharField(max_length=255, blank=True, null=True)
    gross_doctor_name = models.CharField(max_length=255, blank=True, null=True)
    gross_status = models.CharField(max_length=50, blank=True, null=True)
    gross_is_completed = models.BooleanField(blank=True, null=True)
    gross_create_date = models.DateTimeField(blank=True, null=True)
    gross_update_date = models.DateTimeField(blank=True, null=True)
    fk_commande = models.ForeignKey(LlxCommande, models.DO_NOTHING, db_column='fk_commande', blank=True, null=True)
    fk_doctor_user = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_doctor_user', blank=True, null=True)
    fk_gross_assistant_user = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_gross_assistant_user', related_name='llxgross_fk_gross_assistant_user_set', blank=True, null=True)
    gross_created_user = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='gross_created_user', related_name='llxgross_gross_created_user_set', blank=True, null=True)
    gross_updated_user = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='gross_updated_user', related_name='llxgross_gross_updated_user_set', blank=True, null=True)
    batch = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_gross'


class LlxGrossAssign(models.Model):
    assign_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=255, blank=True, null=True)
    gross_assistant_name = models.CharField(max_length=255, blank=True, null=True)
    gross_doctor_name = models.CharField(max_length=255, blank=True, null=True)
    gross_status = models.CharField(max_length=50, blank=True, null=True)
    gross_assign_created_user = models.CharField(max_length=255, blank=True, null=True)
    gross_assign_updated_user = models.CharField(max_length=255, blank=True, null=True)
    assign_create_date = models.DateTimeField(blank=True, null=True)
    assign_update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_gross_assign'


class LlxGrossSpecimen(models.Model):
    specimen_id = models.AutoField(primary_key=True)
    fk_gross_id = models.CharField(max_length=255, blank=True, null=True)
    specimen = models.CharField(max_length=1000, blank=True, null=True)
    gross_description = models.CharField(max_length=2000, blank=True, null=True)
    update_user = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_gross_specimen'


class LlxGrossSpecimenHistory(models.Model):
    rowid = models.AutoField(primary_key=True)
    specimen_id = models.CharField(max_length=255, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=255, blank=True, null=True)
    specimen = models.CharField(max_length=1000, blank=True, null=True)
    gross_description = models.CharField(max_length=20000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_gross_specimen_history'


class LlxGrossSpecimenSection(models.Model):
    gross_specimen_section_id = models.AutoField(primary_key=True)
    fk_gross_id = models.CharField(max_length=255, blank=True, null=True)
    section_code = models.CharField(max_length=255, blank=True, null=True)
    specimen_section_description = models.CharField(max_length=900, blank=True, null=True)
    cassettes_numbers = models.CharField(max_length=255, blank=True, null=True)
    tissue = models.CharField(max_length=200, blank=True, null=True)
    bone = models.CharField(max_length=255, blank=True, null=True)
    boneslide = models.CharField(max_length=255, blank=True, null=True)
    re_gross = models.CharField(max_length=255, blank=True, null=True)
    requires_slide_for_block = models.CharField(max_length=255, blank=True, null=True)
    decalcified_bone = models.CharField(max_length=255, blank=True, null=True)
    update_user = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_gross_specimen_section'


class LlxGrossSpecimenSectionHistory(models.Model):
    rowid = models.AutoField(primary_key=True)
    gross_specimen_section_id = models.CharField(max_length=255, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=255, blank=True, null=True)
    section_code = models.CharField(max_length=255, blank=True, null=True)
    specimen_section_description = models.CharField(max_length=900, blank=True, null=True)
    cassettes_numbers = models.CharField(max_length=255, blank=True, null=True)
    tissue = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_gross_specimen_section_history'


class LlxGrossSpecimenUsed(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_gross_id = models.IntegerField()
    section_code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_gross_specimen_used'


class LlxGrossSummaryOfSection(models.Model):
    gross_summary_id = models.AutoField(primary_key=True)
    fk_gross_id = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=900, blank=True, null=True)
    ink_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_gross_summary_of_section'


class LlxGrossSummaryOfSectionHistory(models.Model):
    rowid = models.AutoField(primary_key=True)
    gross_summary_id = models.CharField(max_length=255, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=255, blank=True, null=True)
    ink_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_gross_summary_of_section_history'


class LlxGrossmoduleGross(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=128)
    label = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_project = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField()
    tms = models.DateTimeField(blank=True, null=True)
    fk_user_creat = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_grossmodule_gross'


class LlxHoliday(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField()
    fk_user = models.IntegerField()
    fk_user_create = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_type = models.IntegerField()
    date_create = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField()
    halfday = models.IntegerField(blank=True, null=True)
    statut = models.IntegerField()
    fk_validator = models.IntegerField()
    date_valid = models.DateTimeField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    date_approve = models.DateTimeField(blank=True, null=True)
    fk_user_approve = models.IntegerField(blank=True, null=True)
    date_refuse = models.DateTimeField(blank=True, null=True)
    fk_user_refuse = models.IntegerField(blank=True, null=True)
    date_cancel = models.DateTimeField(blank=True, null=True)
    fk_user_cancel = models.IntegerField(blank=True, null=True)
    detail_refuse = models.CharField(max_length=250, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    tms = models.DateTimeField()
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    nb_open_day = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_holiday'


class LlxHolidayConfig(models.Model):
    rowid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=128)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_holiday_config'


class LlxHolidayExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_holiday_extrafields'


class LlxHolidayLogs(models.Model):
    rowid = models.AutoField(primary_key=True)
    date_action = models.DateTimeField(blank=True, null=True)
    fk_user_action = models.IntegerField()
    fk_user_update = models.IntegerField()
    fk_type = models.IntegerField()
    type_action = models.CharField(max_length=255)
    prev_solde = models.CharField(max_length=255)
    new_solde = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'llx_holiday_logs'


class LlxHolidayUsers(models.Model):
    fk_user = models.IntegerField()
    fk_type = models.IntegerField()
    nb_holiday = models.FloatField()

    class Meta:
        managed = False
        db_table = 'llx_holiday_users'
        unique_together = (('fk_user', 'fk_type'),)


class LlxImportModel(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    fk_user = models.IntegerField()
    label = models.CharField(max_length=50)
    type = models.CharField(max_length=64)
    field = models.TextField()

    class Meta:
        managed = False
        db_table = 'llx_import_model'
        unique_together = (('label', 'type'),)


class LlxIntracommreport(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    type_declaration = models.CharField(max_length=32, blank=True, null=True)
    periods = models.CharField(max_length=32, blank=True, null=True)
    mode = models.CharField(max_length=32, blank=True, null=True)
    content_xml = models.TextField(blank=True, null=True)
    type_export = models.CharField(max_length=10, blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_intracommreport'


class LlxInventory(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=48, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_warehouse = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    date_inventory = models.DateTimeField(blank=True, null=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_inventory'
        unique_together = (('ref', 'entity'),)


class LlxInventoryExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_inventory_extrafields'


class LlxInventorydet(models.Model):
    rowid = models.AutoField(primary_key=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_inventory = models.IntegerField(blank=True, null=True)
    fk_warehouse = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    batch = models.CharField(max_length=128, blank=True, null=True)
    qty_stock = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    qty_view = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    qty_regulated = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fk_movement = models.IntegerField(blank=True, null=True)
    pmp_real = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    pmp_expected = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_inventorydet'
        unique_together = (('fk_inventory', 'fk_warehouse', 'fk_product', 'batch'),)


class LlxKnowledgemanagementKnowledgerecord(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=128)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=6, blank=True, null=True)
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat')
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    fk_ticket = models.IntegerField(blank=True, null=True)
    fk_c_ticket_category = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_knowledgemanagement_knowledgerecord'


class LlxKnowledgemanagementKnowledgerecordExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_knowledgemanagement_knowledgerecord_extrafields'


class LlxLinks(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    datea = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    objecttype = models.CharField(max_length=255)
    objectid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_links'
        unique_together = (('objectid', 'label'),)


class LlxLoan(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    label = models.CharField(max_length=80)
    fk_bank = models.IntegerField(blank=True, null=True)
    capital = models.DecimalField(max_digits=24, decimal_places=8)
    insurance_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    datestart = models.DateField(blank=True, null=True)
    dateend = models.DateField(blank=True, null=True)
    nbterm = models.FloatField(blank=True, null=True)
    rate = models.DecimalField(max_digits=65535, decimal_places=65535)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    capital_position = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    date_position = models.DateField(blank=True, null=True)
    paid = models.SmallIntegerField()
    accountancy_account_capital = models.CharField(max_length=32, blank=True, null=True)
    accountancy_account_insurance = models.CharField(max_length=32, blank=True, null=True)
    accountancy_account_interest = models.CharField(max_length=32, blank=True, null=True)
    fk_projet = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    active = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_loan'


class LlxLoanSchedule(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_loan = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    datep = models.DateTimeField(blank=True, null=True)
    amount_capital = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    amount_insurance = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    amount_interest = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_typepayment = models.IntegerField()
    num_payment = models.CharField(max_length=50, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField()
    fk_payment_loan = models.IntegerField(blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_loan_schedule'
        unique_together = (('fk_loan', 'datep'),)


class LlxLocaltax(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    localtaxtype = models.SmallIntegerField(blank=True, null=True)
    tms = models.DateTimeField()
    datep = models.DateField(blank=True, null=True)
    datev = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField(blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_localtax'


class LlxMailing(models.Model):
    rowid = models.AutoField(primary_key=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    titre = models.CharField(max_length=128, blank=True, null=True)
    entity = models.IntegerField()
    sujet = models.CharField(max_length=128, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    bgcolor = models.CharField(max_length=8, blank=True, null=True)
    bgimage = models.CharField(max_length=255, blank=True, null=True)
    cible = models.CharField(max_length=60, blank=True, null=True)
    nbemail = models.IntegerField(blank=True, null=True)
    email_from = models.CharField(max_length=160, blank=True, null=True)
    email_replyto = models.CharField(max_length=160, blank=True, null=True)
    email_errorsto = models.CharField(max_length=160, blank=True, null=True)
    tag = models.CharField(max_length=128, blank=True, null=True)
    date_creat = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    date_appro = models.DateTimeField(blank=True, null=True)
    date_envoi = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_user_appro = models.IntegerField(blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    joined_file1 = models.CharField(max_length=255, blank=True, null=True)
    joined_file2 = models.CharField(max_length=255, blank=True, null=True)
    joined_file3 = models.CharField(max_length=255, blank=True, null=True)
    joined_file4 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_mailing'
        unique_together = (('titre', 'entity'),)


class LlxMailingAdvtarget(models.Model):
    rowid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=180)
    entity = models.IntegerField()
    fk_element = models.IntegerField()
    type_element = models.CharField(max_length=180)
    filtervalue = models.TextField(blank=True, null=True)
    fk_user_author = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    fk_user_mod = models.IntegerField()
    tms = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_mailing_advtarget'


class LlxMailingCibles(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_mailing = models.IntegerField()
    fk_contact = models.IntegerField()
    lastname = models.CharField(max_length=160, blank=True, null=True)
    firstname = models.CharField(max_length=160, blank=True, null=True)
    email = models.CharField(max_length=160)
    other = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=64, blank=True, null=True)
    statut = models.SmallIntegerField()
    source_url = models.CharField(max_length=255, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    source_type = models.CharField(max_length=16, blank=True, null=True)
    date_envoi = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    error_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_mailing_cibles'
        unique_together = (('fk_mailing', 'email'),)


class LlxMailingUnsubscribe(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    email = models.CharField(max_length=255, blank=True, null=True)
    unsubscribegroup = models.CharField(max_length=128, blank=True, null=True)
    ip = models.CharField(max_length=128, blank=True, null=True)
    date_creat = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_mailing_unsubscribe'
        unique_together = (('email', 'entity', 'unsubscribegroup'),)


class LlxManualProcessor(models.Model):
    rowid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    batch_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_manual_processor'


class LlxMenu(models.Model):
    rowid = models.AutoField(primary_key=True)
    menu_handler = models.CharField(max_length=16)
    entity = models.IntegerField()
    module = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=4)
    mainmenu = models.CharField(max_length=100)
    leftmenu = models.CharField(max_length=100, blank=True, null=True)
    fk_menu = models.IntegerField()
    fk_mainmenu = models.CharField(max_length=100, blank=True, null=True)
    fk_leftmenu = models.CharField(max_length=100, blank=True, null=True)
    position = models.IntegerField()
    url = models.CharField(max_length=255)
    target = models.CharField(max_length=100, blank=True, null=True)
    titre = models.CharField(max_length=255)
    prefix = models.CharField(max_length=255, blank=True, null=True)
    langs = models.CharField(max_length=100, blank=True, null=True)
    level = models.SmallIntegerField(blank=True, null=True)
    perms = models.TextField(blank=True, null=True)
    enabled = models.TextField(blank=True, null=True)
    usertype = models.IntegerField()
    tms = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_menu'
        unique_together = (('menu_handler', 'fk_menu', 'position', 'url', 'entity'),)


class LlxMfc(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    previous_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_mfc'


class LlxMicro(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    specimen = models.CharField(max_length=550, blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    histologic_type = models.CharField(max_length=500, blank=True, null=True)
    hitologic_grade = models.CharField(max_length=500, blank=True, null=True)
    pattern_of_growth = models.CharField(max_length=500, blank=True, null=True)
    stromal_reaction = models.CharField(max_length=500, blank=True, null=True)
    depth_of_invasion = models.CharField(max_length=500, blank=True, null=True)
    lymphovascular_invasion = models.CharField(max_length=500, blank=True, null=True)
    perineural_invasion = models.CharField(max_length=500, blank=True, null=True)
    bone = models.CharField(max_length=500, blank=True, null=True)
    lim_node = models.CharField(max_length=500, blank=True, null=True)
    ptnm_title = models.CharField(max_length=500, blank=True, null=True)
    pt2 = models.CharField(max_length=500, blank=True, null=True)
    pnx = models.CharField(max_length=500, blank=True, null=True)
    pmx = models.CharField(max_length=500, blank=True, null=True)
    resection_margin = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_micro'


class LlxMicroHistory(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    specimen = models.CharField(max_length=550, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_micro_history'


class LlxMrpMo(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=128)
    mrptype = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    qty = models.FloatField()
    fk_warehouse = models.IntegerField(blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat')
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    fk_product = models.IntegerField()
    date_start_planned = models.DateTimeField(blank=True, null=True)
    date_end_planned = models.DateTimeField(blank=True, null=True)
    fk_bom = models.IntegerField(blank=True, null=True)
    fk_project = models.IntegerField(blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    fk_parent_line = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_mrp_mo'


class LlxMrpMoExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_mrp_mo_extrafields'


class LlxMrpProduction(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_mo = models.ForeignKey(LlxMrpMo, models.DO_NOTHING, db_column='fk_mo')
    origin_id = models.IntegerField(blank=True, null=True)
    origin_type = models.CharField(max_length=10, blank=True, null=True)
    position = models.IntegerField()
    fk_product = models.ForeignKey('LlxProduct', models.DO_NOTHING, db_column='fk_product')
    fk_warehouse = models.IntegerField(blank=True, null=True)
    qty = models.FloatField()
    qty_frozen = models.SmallIntegerField(blank=True, null=True)
    disable_stock_change = models.SmallIntegerField(blank=True, null=True)
    batch = models.CharField(max_length=128, blank=True, null=True)
    role = models.CharField(max_length=10, blank=True, null=True)
    fk_mrp_production = models.IntegerField(blank=True, null=True)
    fk_stock_movement = models.ForeignKey('LlxStockMouvement', models.DO_NOTHING, db_column='fk_stock_movement', blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_mrp_production'


class LlxMulticurrency(models.Model):
    rowid = models.AutoField(primary_key=True)
    date_create = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_multicurrency'


class LlxMulticurrencyRate(models.Model):
    rowid = models.AutoField(primary_key=True)
    date_sync = models.DateTimeField(blank=True, null=True)
    rate = models.DecimalField(max_digits=65535, decimal_places=65535)
    fk_multicurrency = models.IntegerField()
    entity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_multicurrency_rate'


class LlxNotify(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    daten = models.DateTimeField(blank=True, null=True)
    fk_action = models.IntegerField()
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_contact = models.IntegerField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=16, blank=True, null=True)
    type_target = models.CharField(max_length=16, blank=True, null=True)
    objet_type = models.CharField(max_length=24)
    objet_id = models.IntegerField()
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_notify'


class LlxNotifyDef(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    datec = models.DateField(blank=True, null=True)
    fk_action = models.IntegerField()
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_contact = models.IntegerField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_notify_def'


class LlxNotifyDefObject(models.Model):
    entity = models.IntegerField()
    objet_type = models.CharField(max_length=16, blank=True, null=True)
    objet_id = models.IntegerField()
    type_notif = models.CharField(max_length=16, blank=True, null=True)
    date_notif = models.DateTimeField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    moreparam = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_notify_def_object'


class LlxOauthState(models.Model):
    rowid = models.AutoField(primary_key=True)
    service = models.CharField(max_length=36, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    fk_adherent = models.IntegerField(blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_oauth_state'


class LlxOauthToken(models.Model):
    rowid = models.AutoField(primary_key=True)
    service = models.CharField(max_length=36, blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    tokenstring = models.TextField(blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    fk_adherent = models.IntegerField(blank=True, null=True)
    restricted_ips = models.CharField(max_length=200, blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    entity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_oauth_token'


class LlxObjectLang(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_object = models.IntegerField()
    type_object = models.CharField(max_length=32)
    property = models.CharField(max_length=32)
    lang = models.CharField(max_length=5)
    value = models.TextField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_object_lang'
        unique_together = (('fk_object', 'type_object', 'property', 'lang'),)


class LlxOnlinesignature(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    object_type = models.CharField(max_length=32)
    object_id = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    name = models.CharField(max_length=255)
    ip = models.CharField(max_length=128, blank=True, null=True)
    pathoffile = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_onlinesignature'


class LlxOpensurveyComments(models.Model):
    id_comment = models.AutoField(primary_key=True)
    id_sondage = models.CharField(max_length=16)
    comment = models.TextField()
    tms = models.DateTimeField()
    usercomment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_opensurvey_comments'


class LlxOpensurveyFormquestions(models.Model):
    rowid = models.AutoField(primary_key=True)
    id_sondage = models.CharField(max_length=16, blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    available_answers = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_opensurvey_formquestions'


class LlxOpensurveySondage(models.Model):
    id_sondage = models.CharField(primary_key=True, max_length=16)
    entity = models.IntegerField()
    commentaires = models.TextField(blank=True, null=True)
    mail_admin = models.CharField(max_length=128, blank=True, null=True)
    nom_admin = models.CharField(max_length=64, blank=True, null=True)
    fk_user_creat = models.IntegerField()
    titre = models.TextField()
    date_fin = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=2)
    mailsonde = models.SmallIntegerField()
    allow_comments = models.SmallIntegerField()
    allow_spy = models.SmallIntegerField()
    tms = models.DateTimeField()
    sujet = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_opensurvey_sondage'


class LlxOpensurveyUserFormanswers(models.Model):
    fk_user_survey = models.IntegerField()
    fk_question = models.IntegerField()
    reponses = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_opensurvey_user_formanswers'


class LlxOpensurveyUserStuds(models.Model):
    id_users = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=64)
    id_sondage = models.CharField(max_length=16)
    reponses = models.CharField(max_length=100)
    tms = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_opensurvey_user_studs'


class LlxOtherReport(models.Model):
    rowid = models.AutoField(primary_key=True)
    previous_lab_number = models.CharField(max_length=50, blank=True, null=True)
    report_type = models.CharField(max_length=50, blank=True, null=True)
    new_lab_number = models.CharField(max_length=50, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    previous_report_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_other_report'


class LlxOtherReportClinicalDetails(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    clinical_details = models.TextField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    addressing = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_other_report_clinical_details'


class LlxOtherReportDiagnosis(models.Model):
    rowid = models.CharField(max_length=50, blank=True, null=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    specimen = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_other_report_diagnosis'


class LlxOtherReportGrossSpecimen(models.Model):
    rowid = models.AutoField(primary_key=True)
    specimen_id = models.CharField(max_length=50, blank=True, null=True)
    specimen = models.TextField(blank=True, null=True)
    gross_description = models.TextField(blank=True, null=True)
    fk_gross_id = models.CharField(max_length=50, blank=True, null=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_other_report_gross_specimen'


class LlxOtherReportGrossSpecimenSection(models.Model):
    rowid = models.AutoField(primary_key=True)
    gross_specimen_section_id = models.CharField(max_length=50, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=50, blank=True, null=True)
    section_code = models.CharField(max_length=50, blank=True, null=True)
    specimen_section_description = models.TextField(blank=True, null=True)
    cassettes_numbers = models.CharField(max_length=50, blank=True, null=True)
    tissue = models.CharField(max_length=50, blank=True, null=True)
    bone = models.CharField(max_length=50, blank=True, null=True)
    re_gross = models.CharField(max_length=50, blank=True, null=True)
    requires_slide_for_block = models.CharField(max_length=50, blank=True, null=True)
    decalcified_bone = models.CharField(max_length=50, blank=True, null=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_other_report_gross_specimen_section'


class LlxOtherReportMicro(models.Model):
    rowid = models.CharField(max_length=50, blank=True, null=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    specimen = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_other_report_micro'


class LlxOtherReportPatientInformation(models.Model):
    rowid = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    code_client = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=50, blank=True, null=True)
    ageyrs = models.CharField(max_length=50, blank=True, null=True)
    att_name = models.CharField(max_length=50, blank=True, null=True)
    att_relation = models.CharField(max_length=50, blank=True, null=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_other_report_patient_information'


class LlxOtherReportSiteOfSpecimen(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    site_of_specimen = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_other_report_site_of_specimen'


class LlxOverwriteTrans(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    lang = models.CharField(max_length=5, blank=True, null=True)
    transkey = models.CharField(max_length=128, blank=True, null=True)
    transvalue = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_overwrite_trans'
        unique_together = (('lang', 'transkey', 'entity'),)


class LlxPaiement(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30, blank=True, null=True)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    datep = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_paiement = models.IntegerField()
    num_paiement = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    ext_payment_id = models.CharField(max_length=255, blank=True, null=True)
    ext_payment_site = models.CharField(max_length=128, blank=True, null=True)
    fk_bank = models.IntegerField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    statut = models.SmallIntegerField()
    fk_export_compta = models.IntegerField()
    pos_change = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_paiement'


class LlxPaiementFacture(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_paiement = models.ForeignKey(LlxPaiement, models.DO_NOTHING, db_column='fk_paiement', blank=True, null=True)
    fk_facture = models.ForeignKey(LlxFacture, models.DO_NOTHING, db_column='fk_facture', blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_paiement_facture'
        unique_together = (('fk_paiement', 'fk_facture'),)


class LlxPaiementFactureHistory(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_paiement = models.IntegerField(blank=True, null=True)
    fk_facture = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    change_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_paiement_facture_history'


class LlxPaiementHistory(models.Model):
    rowid = models.AutoField(primary_key=True)
    operation = models.CharField(max_length=10)
    transaction_timestamp = models.DateTimeField(blank=True, null=True)
    old_data = models.JSONField(blank=True, null=True)
    new_data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_paiement_history'


class LlxPaiementcharge(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_charge = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    datep = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_typepaiement = models.IntegerField()
    num_paiement = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_paiementcharge'


class LlxPaiementfourn(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30, blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    datep = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_paiement = models.IntegerField()
    num_paiement = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField()
    statut = models.SmallIntegerField()
    model_pdf = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_paiementfourn'


class LlxPaiementfournFacturefourn(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_paiementfourn = models.IntegerField(blank=True, null=True)
    fk_facturefourn = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_paiementfourn_facturefourn'
        unique_together = (('fk_paiementfourn', 'fk_facturefourn'),)


class LlxPartnership(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=128)
    status = models.SmallIntegerField()
    fk_type = models.IntegerField()
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_member = models.IntegerField(blank=True, null=True)
    date_partnership_start = models.DateField()
    date_partnership_end = models.DateField(blank=True, null=True)
    entity = models.IntegerField()
    reason_decline_or_cancel = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    fk_user_creat = models.IntegerField()
    tms = models.DateTimeField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    count_last_url_check_error = models.IntegerField(blank=True, null=True)
    last_check_backlink = models.DateTimeField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    url_to_check = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_partnership'
        unique_together = (('fk_type', 'fk_member', 'date_partnership_start'), ('fk_type', 'fk_soc', 'date_partnership_start'), ('ref', 'entity'),)


class LlxPartnershipExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_partnership_extrafields'


class LlxPaymentDonation(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_donation = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    datep = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_typepayment = models.IntegerField()
    num_payment = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    ext_payment_id = models.CharField(max_length=255, blank=True, null=True)
    ext_payment_site = models.CharField(max_length=128, blank=True, null=True)
    fk_bank = models.IntegerField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_payment_donation'


class LlxPaymentExpensereport(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_expensereport = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    datep = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_typepayment = models.IntegerField()
    num_payment = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_payment_expensereport'


class LlxPaymentLoan(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_loan = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    datep = models.DateTimeField(blank=True, null=True)
    amount_capital = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    amount_insurance = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    amount_interest = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_typepayment = models.IntegerField()
    num_payment = models.CharField(max_length=50, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_payment_loan'


class LlxPaymentSalary(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30, blank=True, null=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    fk_user = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user', blank=True, null=True)
    datep = models.DateField(blank=True, null=True)
    datev = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    fk_projet = models.IntegerField(blank=True, null=True)
    fk_typepayment = models.IntegerField()
    num_payment = models.CharField(max_length=50, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    datesp = models.DateField(blank=True, null=True)
    dateep = models.DateField(blank=True, null=True)
    entity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_salary = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_payment_salary'


class LlxPaymentVarious(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30, blank=True, null=True)
    num_payment = models.CharField(max_length=50, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    datep = models.DateField(blank=True, null=True)
    datev = models.DateField(blank=True, null=True)
    sens = models.SmallIntegerField()
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    fk_typepayment = models.IntegerField()
    accountancy_code = models.CharField(max_length=32, blank=True, null=True)
    subledger_account = models.CharField(max_length=32, blank=True, null=True)
    fk_projet = models.IntegerField(blank=True, null=True)
    entity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_payment_various'


class LlxPaymentVat(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_tva = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    datep = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_typepaiement = models.IntegerField()
    num_paiement = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_payment_vat'


class LlxPosCashFence(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=64, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    opening = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    cash = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    card = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    cheque = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    day_close = models.IntegerField(blank=True, null=True)
    month_close = models.IntegerField(blank=True, null=True)
    year_close = models.IntegerField(blank=True, null=True)
    posmodule = models.CharField(max_length=30, blank=True, null=True)
    posnumber = models.CharField(max_length=30, blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_pos_cash_fence'


class LlxPrelevementBons(models.Model):
    rowid = models.AutoField(primary_key=True)
    type = models.CharField(max_length=16, blank=True, null=True)
    ref = models.CharField(max_length=12, blank=True, null=True)
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    credite = models.SmallIntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    date_trans = models.DateTimeField(blank=True, null=True)
    method_trans = models.SmallIntegerField(blank=True, null=True)
    fk_user_trans = models.IntegerField(blank=True, null=True)
    date_credit = models.DateTimeField(blank=True, null=True)
    fk_user_credit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_prelevement_bons'
        unique_together = (('ref', 'entity'),)


class LlxPrelevementFacture(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_facture = models.IntegerField(blank=True, null=True)
    fk_facture_fourn = models.IntegerField(blank=True, null=True)
    fk_prelevement_lignes = models.ForeignKey('LlxPrelevementLignes', models.DO_NOTHING, db_column='fk_prelevement_lignes')

    class Meta:
        managed = False
        db_table = 'llx_prelevement_facture'


class LlxPrelevementFactureDemande(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    fk_facture = models.IntegerField(blank=True, null=True)
    fk_facture_fourn = models.IntegerField(blank=True, null=True)
    sourcetype = models.CharField(max_length=32, blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    date_demande = models.DateTimeField(blank=True, null=True)
    traite = models.SmallIntegerField(blank=True, null=True)
    date_traite = models.DateTimeField(blank=True, null=True)
    fk_prelevement_bons = models.IntegerField(blank=True, null=True)
    fk_user_demande = models.IntegerField()
    code_banque = models.CharField(max_length=128, blank=True, null=True)
    code_guichet = models.CharField(max_length=6, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    cle_rib = models.CharField(max_length=5, blank=True, null=True)
    ext_payment_id = models.CharField(max_length=255, blank=True, null=True)
    ext_payment_site = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_prelevement_facture_demande'


class LlxPrelevementLignes(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_prelevement_bons = models.ForeignKey(LlxPrelevementBons, models.DO_NOTHING, db_column='fk_prelevement_bons', blank=True, null=True)
    fk_soc = models.IntegerField()
    statut = models.SmallIntegerField(blank=True, null=True)
    client_nom = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    code_banque = models.CharField(max_length=128, blank=True, null=True)
    code_guichet = models.CharField(max_length=6, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    cle_rib = models.CharField(max_length=5, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_prelevement_lignes'


class LlxPrelevementRejet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_prelevement_lignes = models.IntegerField(blank=True, null=True)
    date_rejet = models.DateTimeField(blank=True, null=True)
    motif = models.IntegerField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    fk_user_creation = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    afacturer = models.SmallIntegerField(blank=True, null=True)
    fk_facture = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_prelevement_rejet'


class LlxPreliminaryReport(models.Model):
    rowid = models.AutoField(primary_key=True)
    test_type = models.CharField(max_length=50, blank=True, null=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    previous_preliminary_report = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_preliminary_report'


class LlxPreliminaryReportDiagnosis(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    specimen = models.TextField(blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_preliminary_report_diagnosis'


class LlxPreliminaryReportDoctorAssistedBySignature(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    doctor_username = models.CharField(max_length=50, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_preliminary_report_doctor_assisted_by_signature'


class LlxPreliminaryReportDoctorFinalizedBySignature(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50, blank=True, null=True)
    doctor_username = models.CharField(max_length=50, blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_preliminary_report_doctor_finalized_by_signature'


class LlxPreliminaryReportMicroscopic(models.Model):
    row_id = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=100, blank=True, null=True)
    fk_gross_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_user = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    specimen = models.TextField(blank=True, null=True)
    updated_user = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_preliminary_report_microscopic'


class LlxPrinterReceipt(models.Model):
    rowid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    fk_type = models.IntegerField(blank=True, null=True)
    fk_profile = models.IntegerField(blank=True, null=True)
    parameter = models.CharField(max_length=128, blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_printer_receipt'


class LlxPrinterReceiptTemplate(models.Model):
    rowid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    template = models.TextField(blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_printer_receipt_template'


class LlxPrinting(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    printer_name = models.TextField()
    printer_location = models.TextField()
    printer_id = models.CharField(max_length=255)
    copy = models.IntegerField()
    module = models.CharField(max_length=16)
    driver = models.CharField(max_length=16)
    userid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_printing'


class LlxProduct(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=128)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=128, blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_parent = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    customcode = models.CharField(max_length=32, blank=True, null=True)
    fk_country = models.ForeignKey(LlxCCountry, models.DO_NOTHING, db_column='fk_country', blank=True, null=True)
    fk_state = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_min = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_min_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_base_type = models.CharField(max_length=3, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    default_vat_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    recuperableonly = models.IntegerField()
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    tosell = models.SmallIntegerField(blank=True, null=True)
    tobuy = models.SmallIntegerField(blank=True, null=True)
    onportal = models.SmallIntegerField(blank=True, null=True)
    tobatch = models.SmallIntegerField()
    batch_mask = models.CharField(max_length=32, blank=True, null=True)
    fk_product_type = models.IntegerField(blank=True, null=True)
    duration = models.CharField(max_length=6, blank=True, null=True)
    seuil_stock_alerte = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=180, blank=True, null=True)
    fk_barcode_type = models.ForeignKey(LlxCBarcodeType, models.DO_NOTHING, db_column='fk_barcode_type', blank=True, null=True)
    accountancy_code_sell = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_sell_intra = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_sell_export = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy_intra = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy_export = models.CharField(max_length=32, blank=True, null=True)
    partnumber = models.CharField(max_length=32, blank=True, null=True)
    net_measure = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    net_measure_units = models.SmallIntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    weight_units = models.SmallIntegerField(blank=True, null=True)
    length = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    length_units = models.SmallIntegerField(blank=True, null=True)
    width = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    width_units = models.SmallIntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    height_units = models.SmallIntegerField(blank=True, null=True)
    surface = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    surface_units = models.SmallIntegerField(blank=True, null=True)
    volume = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    volume_units = models.SmallIntegerField(blank=True, null=True)
    stock = models.FloatField(blank=True, null=True)
    pmp = models.DecimalField(max_digits=24, decimal_places=8)
    fifo = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    lifo = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_default_warehouse = models.ForeignKey(LlxEntrepot, models.DO_NOTHING, db_column='fk_default_warehouse', blank=True, null=True)
    canvas = models.CharField(max_length=32, blank=True, null=True)
    finished = models.ForeignKey(LlxCProductNature, models.DO_NOTHING, db_column='finished', to_field='code', blank=True, null=True)
    lifetime = models.IntegerField(blank=True, null=True)
    qc_frequency = models.IntegerField(blank=True, null=True)
    hidden = models.SmallIntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    fk_price_expression = models.IntegerField(blank=True, null=True)
    desiredstock = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)
    price_autogen = models.SmallIntegerField(blank=True, null=True)
    fk_project = models.IntegerField(blank=True, null=True)
    mandatory_period = models.SmallIntegerField(blank=True, null=True)
    fk_default_bom = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product'
        unique_together = (('barcode', 'fk_barcode_type', 'entity'), ('ref', 'entity'),)


class LlxProductAssociation(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_product_pere = models.IntegerField()
    fk_product_fils = models.IntegerField()
    qty = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    incdec = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_association'
        unique_together = (('fk_product_pere', 'fk_product_fils'),)


class LlxProductAttribute(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(unique=True, max_length=255)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255)
    position = models.IntegerField()
    entity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_product_attribute'


class LlxProductAttributeCombination(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_product_parent = models.IntegerField()
    fk_product_child = models.IntegerField()
    variation_price = models.DecimalField(max_digits=24, decimal_places=8)
    variation_price_percentage = models.IntegerField(blank=True, null=True)
    variation_weight = models.FloatField()
    variation_ref_ext = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_product_attribute_combination'


class LlxProductAttributeCombination2Val(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_prod_combination = models.IntegerField()
    fk_prod_attr = models.IntegerField()
    fk_prod_attr_val = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_product_attribute_combination2val'


class LlxProductAttributeCombinationPriceLevel(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_product_attribute_combination = models.IntegerField()
    fk_price_level = models.IntegerField()
    variation_price = models.DecimalField(max_digits=24, decimal_places=8)
    variation_price_percentage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_attribute_combination_price_level'
        unique_together = (('fk_product_attribute_combination', 'fk_price_level'),)


class LlxProductAttributeValue(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_product_attribute = models.IntegerField()
    ref = models.CharField(max_length=180, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField()
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_product_attribute_value'
        unique_together = (('fk_product_attribute', 'ref'),)


class LlxProductBatch(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_product_stock = models.ForeignKey('LlxProductStock', models.DO_NOTHING, db_column='fk_product_stock')
    eatby = models.DateTimeField(blank=True, null=True)
    sellby = models.DateTimeField(blank=True, null=True)
    batch = models.CharField(max_length=128)
    qty = models.DecimalField(max_digits=65535, decimal_places=65535)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_batch'
        unique_together = (('fk_product_stock', 'batch'),)


class LlxProductCustomerPrice(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_product = models.ForeignKey(LlxProduct, models.DO_NOTHING, db_column='fk_product')
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    ref_customer = models.CharField(max_length=128, blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_min = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_min_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_base_type = models.CharField(max_length=3, blank=True, null=True)
    default_vat_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    recuperableonly = models.IntegerField()
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10)
    fk_user = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user', blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_customer_price'
        unique_together = (('fk_product', 'fk_soc'),)


class LlxProductCustomerPriceLog(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    fk_product = models.IntegerField()
    fk_soc = models.IntegerField()
    ref_customer = models.CharField(max_length=30, blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_min = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_min_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_base_type = models.CharField(max_length=3, blank=True, null=True)
    default_vat_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    recuperableonly = models.IntegerField()
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10)
    fk_user = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_customer_price_log'


class LlxProductExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)
    sys = models.CharField(max_length=255, blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    opr = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_extrafields'


class LlxProductFournisseurPrice(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_product = models.ForeignKey(LlxProduct, models.DO_NOTHING, db_column='fk_product', blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    ref_fourn = models.CharField(max_length=128, blank=True, null=True)
    desc_fourn = models.TextField(blank=True, null=True)
    fk_availability = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    quantity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remise_percent = models.DecimalField(max_digits=65535, decimal_places=65535)
    remise = models.DecimalField(max_digits=65535, decimal_places=65535)
    unitprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    charges = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    default_vat_code = models.CharField(max_length=10, blank=True, null=True)
    barcode = models.CharField(max_length=180, blank=True, null=True)
    fk_barcode_type = models.ForeignKey(LlxCBarcodeType, models.DO_NOTHING, db_column='fk_barcode_type', blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10)
    info_bits = models.IntegerField()
    fk_user = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user', blank=True, null=True)
    fk_supplier_price_expression = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    delivery_time_days = models.IntegerField(blank=True, null=True)
    supplier_reputation = models.CharField(max_length=10, blank=True, null=True)
    packaging = models.FloatField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_unitprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_fournisseur_price'
        unique_together = (('ref_fourn', 'fk_soc', 'quantity', 'entity'),)


class LlxProductFournisseurPriceExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_fournisseur_price_extrafields'


class LlxProductFournisseurPriceLog(models.Model):
    rowid = models.AutoField(primary_key=True)
    datec = models.DateTimeField(blank=True, null=True)
    fk_product_fournisseur = models.IntegerField()
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    quantity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_unitprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_fournisseur_price_log'


class LlxProductLang(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_product = models.ForeignKey(LlxProduct, models.DO_NOTHING, db_column='fk_product')
    lang = models.CharField(max_length=5)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_lang'
        unique_together = (('fk_product', 'lang'),)


class LlxProductLot(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField()
    batch = models.CharField(max_length=128, blank=True, null=True)
    eatby = models.DateField(blank=True, null=True)
    sellby = models.DateField(blank=True, null=True)
    eol_date = models.DateTimeField(blank=True, null=True)
    manufacturing_date = models.DateTimeField(blank=True, null=True)
    scrapping_date = models.DateTimeField(blank=True, null=True)
    barcode = models.CharField(max_length=180, blank=True, null=True)
    fk_barcode_type = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_lot'
        unique_together = (('fk_product', 'batch'),)


class LlxProductLotExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_lot_extrafields'


class LlxProductPerentity(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_product = models.IntegerField(blank=True, null=True)
    entity = models.IntegerField()
    accountancy_code_sell = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_sell_intra = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_sell_export = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy_intra = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy_export = models.CharField(max_length=32, blank=True, null=True)
    pmp = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_perentity'
        unique_together = (('fk_product', 'entity'),)


class LlxProductPrice(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    tms = models.DateTimeField()
    fk_product = models.ForeignKey(LlxProduct, models.DO_NOTHING, db_column='fk_product')
    date_price = models.DateTimeField(blank=True, null=True)
    price_level = models.SmallIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_min = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_min_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_base_type = models.CharField(max_length=3, blank=True, null=True)
    default_vat_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4)
    recuperableonly = models.IntegerField()
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    tosell = models.SmallIntegerField(blank=True, null=True)
    price_by_qty = models.IntegerField()
    fk_price_expression = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_price_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_price'


class LlxProductPriceByQty(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_product_price = models.ForeignKey(LlxProductPrice, models.DO_NOTHING, db_column='fk_product_price')
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_base_type = models.CharField(max_length=3, blank=True, null=True)
    quantity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remise_percent = models.DecimalField(max_digits=65535, decimal_places=65535)
    remise = models.DecimalField(max_digits=65535, decimal_places=65535)
    unitprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_price_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    tms = models.DateTimeField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_price_by_qty'
        unique_together = (('fk_product_price', 'quantity'),)


class LlxProductPricerules(models.Model):
    rowid = models.AutoField(primary_key=True)
    level = models.IntegerField(unique=True)
    fk_level = models.IntegerField()
    var_percent = models.FloatField()
    var_min_percent = models.FloatField()

    class Meta:
        managed = False
        db_table = 'llx_product_pricerules'


class LlxProductStock(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_product = models.IntegerField()
    fk_entrepot = models.IntegerField()
    reel = models.FloatField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_stock'
        unique_together = (('fk_product', 'fk_entrepot'),)


class LlxProductWarehouseProperties(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_product = models.IntegerField()
    fk_entrepot = models.IntegerField()
    seuil_stock_alerte = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    desiredstock = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_product_warehouse_properties'


class LlxProjet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc', blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    dateo = models.DateField(blank=True, null=True)
    datee = models.DateField(blank=True, null=True)
    ref = models.CharField(max_length=50, blank=True, null=True)
    entity = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    fk_user_creat = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    public = models.IntegerField(blank=True, null=True)
    fk_statut = models.IntegerField()
    fk_opp_status = models.IntegerField(blank=True, null=True)
    opp_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fk_opp_status_end = models.IntegerField(blank=True, null=True)
    date_close = models.DateTimeField(blank=True, null=True)
    fk_user_close = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    email_msgid = models.CharField(max_length=175, blank=True, null=True)
    opp_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    budget_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    usage_opportunity = models.IntegerField(blank=True, null=True)
    usage_task = models.IntegerField(blank=True, null=True)
    usage_bill_time = models.IntegerField(blank=True, null=True)
    usage_organize_event = models.IntegerField(blank=True, null=True)
    accept_conference_suggestions = models.IntegerField(blank=True, null=True)
    accept_booth_suggestions = models.IntegerField(blank=True, null=True)
    max_attendees = models.IntegerField(blank=True, null=True)
    price_registration = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    price_booth = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_projet'
        unique_together = (('ref', 'entity'),)


class LlxProjetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_projet_extrafields'


class LlxProjetTask(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=50, blank=True, null=True)
    entity = models.IntegerField()
    fk_projet = models.ForeignKey(LlxProjet, models.DO_NOTHING, db_column='fk_projet')
    fk_task_parent = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    dateo = models.DateTimeField(blank=True, null=True)
    datee = models.DateTimeField(blank=True, null=True)
    datev = models.DateTimeField(blank=True, null=True)
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration_effective = models.FloatField(blank=True, null=True)
    planned_workload = models.FloatField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    budget_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_valid', related_name='llxprojettask_fk_user_valid_set', blank=True, null=True)
    fk_statut = models.SmallIntegerField()
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_projet_task'
        unique_together = (('ref', 'entity'),)


class LlxProjetTaskExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_projet_task_extrafields'


class LlxProjetTaskTime(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_task = models.IntegerField()
    task_date = models.DateField(blank=True, null=True)
    task_datehour = models.DateTimeField(blank=True, null=True)
    task_date_withhour = models.IntegerField(blank=True, null=True)
    task_duration = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    thm = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    invoice_id = models.IntegerField(blank=True, null=True)
    invoice_line_id = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    intervention_id = models.IntegerField(blank=True, null=True)
    intervention_line_id = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_projet_task_time'


class LlxPropal(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_int = models.CharField(max_length=255, blank=True, null=True)
    ref_client = models.CharField(max_length=255, blank=True, null=True)
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc', blank=True, null=True)
    fk_projet = models.ForeignKey(LlxProjet, models.DO_NOTHING, db_column='fk_projet', blank=True, null=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    datep = models.DateField(blank=True, null=True)
    fin_validite = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    date_signature = models.DateTimeField(blank=True, null=True)
    date_cloture = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_valid', related_name='llxpropal_fk_user_valid_set', blank=True, null=True)
    fk_user_signature = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_signature', related_name='llxpropal_fk_user_signature_set', blank=True, null=True)
    fk_user_cloture = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_cloture', related_name='llxpropal_fk_user_cloture_set', blank=True, null=True)
    fk_statut = models.SmallIntegerField()
    price = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise_absolue = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_currency = models.CharField(max_length=3, blank=True, null=True)
    fk_cond_reglement = models.IntegerField(blank=True, null=True)
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    online_sign_ip = models.CharField(max_length=48, blank=True, null=True)
    online_sign_name = models.CharField(max_length=64, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    date_livraison = models.DateField(blank=True, null=True)
    fk_shipping_method = models.IntegerField(blank=True, null=True)
    fk_warehouse = models.IntegerField(blank=True, null=True)
    fk_availability = models.IntegerField(blank=True, null=True)
    fk_input_reason = models.IntegerField(blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    fk_delivery_address = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    deposit_percent = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_propal'
        unique_together = (('ref', 'entity'),)


class LlxPropalExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_propal_extrafields'


class LlxPropalMergePdfProduct(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_product = models.IntegerField()
    file_name = models.CharField(max_length=200)
    lang = models.CharField(max_length=5, blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_mod = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_propal_merge_pdf_product'


class LlxPropaldet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_propal = models.ForeignKey(LlxPropal, models.DO_NOTHING, db_column='fk_propal')
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    qty = models.FloatField(blank=True, null=True)
    remise_percent = models.FloatField(blank=True, null=True)
    remise = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    buy_price_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_product_fournisseur_price = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_propaldet'


class LlxPropaldetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_propaldet_extrafields'


class LlxReGross(models.Model):
    rowid = models.AutoField(primary_key=True)
    lab_number = models.CharField(max_length=50)
    doctor_name = models.CharField(max_length=100)
    gross_assistant_name = models.CharField(max_length=100)
    gross_station = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_re_gross'


class LlxReception(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    fk_soc = models.ForeignKey('LlxSociete', models.DO_NOTHING, db_column='fk_soc')
    fk_projet = models.IntegerField(blank=True, null=True)
    ref_ext = models.CharField(max_length=30, blank=True, null=True)
    ref_int = models.CharField(max_length=30, blank=True, null=True)
    ref_supplier = models.CharField(max_length=128, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_author', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    fk_user_valid = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_valid', related_name='llxreception_fk_user_valid_set', blank=True, null=True)
    date_delivery = models.DateTimeField(blank=True, null=True)
    date_reception = models.DateTimeField(blank=True, null=True)
    fk_shipping_method = models.ForeignKey(LlxCShipmentMode, models.DO_NOTHING, db_column='fk_shipping_method', blank=True, null=True)
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    fk_statut = models.SmallIntegerField(blank=True, null=True)
    billed = models.SmallIntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    width = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    size_units = models.IntegerField(blank=True, null=True)
    size = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    weight_units = models.IntegerField(blank=True, null=True)
    weight = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_reception'
        unique_together = (('ref', 'entity'),)


class LlxReceptionExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_reception_extrafields'


class LlxRecruitmentRecruitmentcandidature(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=128)
    fk_recruitmentjobposition = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat')
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()
    firstname = models.CharField(max_length=128, blank=True, null=True)
    lastname = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
    remuneration_requested = models.IntegerField(blank=True, null=True)
    remuneration_proposed = models.IntegerField(blank=True, null=True)
    email_msgid = models.CharField(unique=True, max_length=175, blank=True, null=True)
    fk_recruitment_origin = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_recruitment_recruitmentcandidature'


class LlxRecruitmentRecruitmentcandidatureExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_recruitment_recruitmentcandidature_extrafields'


class LlxRecruitmentRecruitmentjobposition(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=128)
    entity = models.IntegerField()
    label = models.CharField(max_length=255)
    qty = models.IntegerField()
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_project = models.IntegerField(blank=True, null=True)
    fk_user_recruiter = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_recruiter', blank=True, null=True)
    email_recruiter = models.CharField(max_length=255, blank=True, null=True)
    fk_user_supervisor = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_supervisor', related_name='llxrecruitmentrecruitmentjobposition_fk_user_supervisor_set', blank=True, null=True)
    fk_establishment = models.ForeignKey(LlxEstablishment, models.DO_NOTHING, db_column='fk_establishment', blank=True, null=True)
    date_planned = models.DateField(blank=True, null=True)
    remuneration_suggested = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat', related_name='llxrecruitmentrecruitmentjobposition_fk_user_creat_set')
    fk_user_modif = models.IntegerField(blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_recruitment_recruitmentjobposition'


class LlxRecruitmentRecruitmentjobpositionExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_recruitment_recruitmentjobposition_extrafields'


class LlxResource(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=255, blank=True, null=True)
    asset_number = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fk_code_type_resource = models.CharField(max_length=32, blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_statut = models.SmallIntegerField()
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    fk_country = models.ForeignKey(LlxCCountry, models.DO_NOTHING, db_column='fk_country', blank=True, null=True)
    tms = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'llx_resource'
        unique_together = (('ref', 'entity'),)


class LlxResourceExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_resource_extrafields'


class LlxRightsDef(models.Model):
    pk = models.CompositePrimaryKey('id', 'entity')
    id = models.IntegerField()
    libelle = models.CharField(max_length=255, blank=True, null=True)
    module = models.CharField(max_length=64, blank=True, null=True)
    module_position = models.IntegerField()
    family_position = models.IntegerField()
    entity = models.IntegerField()
    perms = models.CharField(max_length=50, blank=True, null=True)
    subperms = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    bydefault = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_rights_def'
        unique_together = (('id', 'entity'),)


class LlxSalary(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30, blank=True, null=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    fk_user = models.IntegerField()
    datep = models.DateField(blank=True, null=True)
    datev = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    fk_projet = models.IntegerField(blank=True, null=True)
    fk_typepayment = models.IntegerField()
    num_payment = models.CharField(max_length=50, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    datesp = models.DateField(blank=True, null=True)
    dateep = models.DateField(blank=True, null=True)
    entity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    fk_bank = models.IntegerField(blank=True, null=True)
    paye = models.SmallIntegerField()
    fk_account = models.IntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_salary'


class LlxSalaryExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_salary_extrafields'


class LlxSession(models.Model):
    session_id = models.CharField(primary_key=True, max_length=50)
    session_variable = models.TextField(blank=True, null=True)
    last_accessed = models.DateTimeField(blank=True, null=True)
    fk_user = models.IntegerField()
    remote_ip = models.CharField(max_length=64, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_session'


class LlxSociete(models.Model):
    rowid = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=128, blank=True, null=True)
    name_alias = models.CharField(max_length=128, blank=True, null=True)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_int = models.CharField(max_length=255, blank=True, null=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    code_client = models.CharField(max_length=24, blank=True, null=True)
    code_fournisseur = models.CharField(max_length=24, blank=True, null=True)
    code_compta = models.CharField(max_length=24, blank=True, null=True)
    code_compta_fournisseur = models.CharField(max_length=24, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=25, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    fk_departement = models.IntegerField(blank=True, null=True)
    fk_pays = models.IntegerField(blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    socialnetworks = models.TextField(blank=True, null=True)
    fk_effectif = models.IntegerField(blank=True, null=True)
    fk_typent = models.IntegerField(blank=True, null=True)
    fk_forme_juridique = models.IntegerField(blank=True, null=True)
    fk_currency = models.CharField(max_length=3, blank=True, null=True)
    siren = models.CharField(max_length=128, blank=True, null=True)
    siret = models.CharField(max_length=128, blank=True, null=True)
    ape = models.CharField(max_length=128, blank=True, null=True)
    idprof4 = models.CharField(max_length=128, blank=True, null=True)
    idprof5 = models.CharField(max_length=128, blank=True, null=True)
    idprof6 = models.CharField(max_length=128, blank=True, null=True)
    tva_intra = models.CharField(max_length=20, blank=True, null=True)
    capital = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_stcomm = models.IntegerField()
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    prefix_comm = models.CharField(max_length=5, blank=True, null=True)
    client = models.SmallIntegerField(blank=True, null=True)
    fournisseur = models.SmallIntegerField(blank=True, null=True)
    supplier_account = models.CharField(max_length=32, blank=True, null=True)
    fk_prospectlevel = models.CharField(max_length=12, blank=True, null=True)
    fk_incoterms = models.IntegerField(blank=True, null=True)
    location_incoterms = models.CharField(max_length=255, blank=True, null=True)
    customer_bad = models.SmallIntegerField(blank=True, null=True)
    customer_rate = models.FloatField(blank=True, null=True)
    supplier_rate = models.FloatField(blank=True, null=True)
    remise_client = models.FloatField(blank=True, null=True)
    remise_supplier = models.FloatField(blank=True, null=True)
    mode_reglement = models.SmallIntegerField(blank=True, null=True)
    cond_reglement = models.SmallIntegerField(blank=True, null=True)
    transport_mode = models.SmallIntegerField(blank=True, null=True)
    mode_reglement_supplier = models.SmallIntegerField(blank=True, null=True)
    cond_reglement_supplier = models.SmallIntegerField(blank=True, null=True)
    transport_mode_supplier = models.SmallIntegerField(blank=True, null=True)
    fk_shipping_method = models.IntegerField(blank=True, null=True)
    tva_assuj = models.SmallIntegerField(blank=True, null=True)
    localtax1_assuj = models.SmallIntegerField(blank=True, null=True)
    localtax1_value = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_assuj = models.SmallIntegerField(blank=True, null=True)
    localtax2_value = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    barcode = models.CharField(max_length=180, blank=True, null=True)
    fk_barcode_type = models.IntegerField(blank=True, null=True)
    price_level = models.IntegerField(blank=True, null=True)
    outstanding_limit = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    order_min_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    supplier_order_min_amount = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    default_lang = models.CharField(max_length=6, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    logo_squarred = models.CharField(max_length=255, blank=True, null=True)
    canvas = models.CharField(max_length=32, blank=True, null=True)
    fk_warehouse = models.IntegerField(blank=True, null=True)
    webservices_url = models.CharField(max_length=255, blank=True, null=True)
    webservices_key = models.CharField(max_length=128, blank=True, null=True)
    accountancy_code_sell = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy = models.CharField(max_length=32, blank=True, null=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    deposit_percent = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe'
        unique_together = (('barcode', 'fk_barcode_type', 'entity'), ('code_client', 'entity'), ('code_fournisseur', 'entity'), ('prefix_comm', 'entity'),)


class LlxSocieteAccount(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField(blank=True, null=True)
    login = models.CharField(max_length=128)
    pass_encoding = models.CharField(max_length=24, blank=True, null=True)
    pass_crypted = models.CharField(max_length=128, blank=True, null=True)
    pass_temp = models.CharField(max_length=128, blank=True, null=True)
    fk_soc = models.ForeignKey(LlxSociete, models.DO_NOTHING, db_column='fk_soc', blank=True, null=True)
    fk_website = models.IntegerField(blank=True, null=True)
    site = models.CharField(max_length=128, blank=True, null=True)
    site_account = models.CharField(max_length=128, blank=True, null=True)
    key_account = models.CharField(max_length=128, blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_last_login = models.DateTimeField(blank=True, null=True)
    date_previous_login = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField()
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_account'
        unique_together = (('entity', 'fk_soc', 'key_account', 'site', 'fk_website'), ('entity', 'fk_soc', 'login', 'site', 'fk_website'),)


class LlxSocieteAddress(models.Model):
    rowid = models.AutoField(primary_key=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    label = models.CharField(max_length=30, blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    fk_pays = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_address'


class LlxSocieteCommerciaux(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_commerciaux'
        unique_together = (('fk_soc', 'fk_user'),)


class LlxSocieteContacts(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    date_creation = models.DateTimeField(blank=True, null=True)
    fk_soc = models.ForeignKey(LlxSociete, models.DO_NOTHING, db_column='fk_soc')
    fk_c_type_contact = models.ForeignKey(LlxCTypeContact, models.DO_NOTHING, db_column='fk_c_type_contact')
    fk_socpeople = models.ForeignKey('LlxSocpeople', models.DO_NOTHING, db_column='fk_socpeople')
    tms = models.DateTimeField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_contacts'
        unique_together = (('entity', 'fk_soc', 'fk_c_type_contact', 'fk_socpeople'),)


class LlxSocieteExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField(unique=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=255, blank=True, null=True)
    att_name = models.CharField(max_length=255, blank=True, null=True)
    att_relation = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    ageyrs = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_extrafields'


class LlxSocietePerentity(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    entity = models.IntegerField()
    accountancy_code_customer = models.CharField(max_length=24, blank=True, null=True)
    accountancy_code_supplier = models.CharField(max_length=24, blank=True, null=True)
    accountancy_code_sell = models.CharField(max_length=32, blank=True, null=True)
    accountancy_code_buy = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_perentity'
        unique_together = (('fk_soc', 'entity'),)


class LlxSocietePrices(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    price_level = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_prices'


class LlxSocieteRemise(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    fk_soc = models.IntegerField()
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    remise_client = models.DecimalField(max_digits=7, decimal_places=4)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_remise'


class LlxSocieteRemiseExcept(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    fk_soc = models.ForeignKey(LlxSociete, models.DO_NOTHING, db_column='fk_soc')
    discount_type = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    amount_ht = models.DecimalField(max_digits=24, decimal_places=8)
    amount_tva = models.DecimalField(max_digits=24, decimal_places=8)
    amount_ttc = models.DecimalField(max_digits=24, decimal_places=8)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    fk_user = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user')
    fk_facture_line = models.ForeignKey(LlxFacturedet, models.DO_NOTHING, db_column='fk_facture_line', blank=True, null=True)
    fk_facture = models.ForeignKey(LlxFacture, models.DO_NOTHING, db_column='fk_facture', blank=True, null=True)
    fk_facture_source = models.ForeignKey(LlxFacture, models.DO_NOTHING, db_column='fk_facture_source', related_name='llxsocieteremiseexcept_fk_facture_source_set', blank=True, null=True)
    fk_invoice_supplier_line = models.ForeignKey(LlxFactureFournDet, models.DO_NOTHING, db_column='fk_invoice_supplier_line', blank=True, null=True)
    fk_invoice_supplier = models.ForeignKey(LlxFactureFourn, models.DO_NOTHING, db_column='fk_invoice_supplier', blank=True, null=True)
    fk_invoice_supplier_source = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    multicurrency_amount_ht = models.DecimalField(max_digits=24, decimal_places=8)
    multicurrency_amount_tva = models.DecimalField(max_digits=24, decimal_places=8)
    multicurrency_amount_ttc = models.DecimalField(max_digits=24, decimal_places=8)

    class Meta:
        managed = False
        db_table = 'llx_societe_remise_except'


class LlxSocieteRemiseSupplier(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    fk_soc = models.IntegerField()
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    remise_supplier = models.DecimalField(max_digits=7, decimal_places=4)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_remise_supplier'


class LlxSocieteRib(models.Model):
    rowid = models.AutoField(primary_key=True)
    type = models.CharField(max_length=32)
    label = models.CharField(max_length=200, blank=True, null=True)
    fk_soc = models.ForeignKey(LlxSociete, models.DO_NOTHING, db_column='fk_soc')
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    bank = models.CharField(max_length=255, blank=True, null=True)
    code_banque = models.CharField(max_length=128, blank=True, null=True)
    code_guichet = models.CharField(max_length=6, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    cle_rib = models.CharField(max_length=5, blank=True, null=True)
    bic = models.CharField(max_length=20, blank=True, null=True)
    iban_prefix = models.CharField(max_length=34, blank=True, null=True)
    domiciliation = models.CharField(max_length=255, blank=True, null=True)
    proprio = models.CharField(max_length=60, blank=True, null=True)
    owner_address = models.CharField(max_length=255, blank=True, null=True)
    default_rib = models.SmallIntegerField()
    rum = models.CharField(max_length=32, blank=True, null=True)
    date_rum = models.DateField(blank=True, null=True)
    frstrecur = models.CharField(max_length=16, blank=True, null=True)
    last_four = models.CharField(max_length=4, blank=True, null=True)
    card_type = models.CharField(max_length=255, blank=True, null=True)
    cvn = models.CharField(max_length=255, blank=True, null=True)
    exp_date_month = models.IntegerField(blank=True, null=True)
    exp_date_year = models.IntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    approved = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    ending_date = models.DateField(blank=True, null=True)
    max_total_amount_of_all_payments = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    preapproval_key = models.CharField(max_length=255, blank=True, null=True)
    starting_date = models.DateField(blank=True, null=True)
    total_amount_of_all_payments = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    stripe_card_ref = models.CharField(max_length=128, blank=True, null=True)
    stripe_account = models.CharField(max_length=128, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    ipaddress = models.CharField(max_length=68, blank=True, null=True)
    status = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_societe_rib'
        unique_together = (('label', 'fk_soc'),)


class LlxSocpeople(models.Model):
    rowid = models.AutoField(primary_key=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_soc = models.ForeignKey(LlxSociete, models.DO_NOTHING, db_column='fk_soc', blank=True, null=True)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    civility = models.CharField(max_length=6, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=25, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    fk_departement = models.IntegerField(blank=True, null=True)
    fk_pays = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    poste = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    phone_perso = models.CharField(max_length=30, blank=True, null=True)
    phone_mobile = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    socialnetworks = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    no_email = models.SmallIntegerField()
    priv = models.SmallIntegerField()
    fk_prospectcontactlevel = models.CharField(max_length=12, blank=True, null=True)
    fk_stcommcontact = models.IntegerField()
    fk_user_creat = models.ForeignKey('LlxUser', models.DO_NOTHING, db_column='fk_user_creat', blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    default_lang = models.CharField(max_length=6, blank=True, null=True)
    canvas = models.CharField(max_length=32, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    statut = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'llx_socpeople'


class LlxSocpeopleExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_socpeople_extrafields'


class LlxSocpeopleExtrafieldsHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    operation_type = models.CharField(max_length=10)
    rowid = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField(blank=True, null=True)
    fk_object = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_socpeople_extrafields_history'


class LlxSocpeopleHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    operation_type = models.CharField(max_length=10)
    rowid = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField(blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    civility = models.CharField(max_length=6, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=25, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    fk_departement = models.IntegerField(blank=True, null=True)
    fk_pays = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    poste = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    phone_perso = models.CharField(max_length=30, blank=True, null=True)
    phone_mobile = models.CharField(max_length=30, blank=True, null=True)
    fax = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    socialnetworks = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    no_email = models.SmallIntegerField(blank=True, null=True)
    priv = models.SmallIntegerField(blank=True, null=True)
    fk_prospectcontactlevel = models.CharField(max_length=12, blank=True, null=True)
    fk_stcommcontact = models.IntegerField(blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    default_lang = models.CharField(max_length=6, blank=True, null=True)
    canvas = models.CharField(max_length=32, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_socpeople_history'


class LlxStockMouvement(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    datem = models.DateTimeField(blank=True, null=True)
    fk_product = models.IntegerField()
    batch = models.CharField(max_length=128, blank=True, null=True)
    eatby = models.DateField(blank=True, null=True)
    sellby = models.DateField(blank=True, null=True)
    fk_entrepot = models.IntegerField()
    value = models.FloatField(blank=True, null=True)
    price = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    type_mouvement = models.SmallIntegerField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    inventorycode = models.CharField(max_length=128, blank=True, null=True)
    fk_project = models.IntegerField(blank=True, null=True)
    fk_origin = models.IntegerField(blank=True, null=True)
    origintype = models.CharField(max_length=64, blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    fk_projet = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_stock_mouvement'


class LlxStockMouvementExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_stock_mouvement_extrafields'


class LlxSubscription(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    fk_adherent = models.IntegerField(blank=True, null=True)
    fk_type = models.IntegerField(blank=True, null=True)
    dateadh = models.DateTimeField(blank=True, null=True)
    datef = models.DateTimeField(blank=True, null=True)
    subscription = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_bank = models.IntegerField(blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_subscription'
        unique_together = (('fk_adherent', 'dateadh'),)


class LlxSupplierProposal(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=30)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=255, blank=True, null=True)
    ref_int = models.CharField(max_length=255, blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_projet = models.IntegerField(blank=True, null=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    date_valid = models.DateTimeField(blank=True, null=True)
    date_cloture = models.DateTimeField(blank=True, null=True)
    fk_user_author = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    fk_user_valid = models.IntegerField(blank=True, null=True)
    fk_user_cloture = models.IntegerField(blank=True, null=True)
    fk_statut = models.SmallIntegerField()
    price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remise_percent = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remise_absolue = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remise = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_account = models.IntegerField(blank=True, null=True)
    fk_currency = models.CharField(max_length=3, blank=True, null=True)
    fk_cond_reglement = models.IntegerField(blank=True, null=True)
    fk_mode_reglement = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    last_main_doc = models.CharField(max_length=255, blank=True, null=True)
    date_livraison = models.DateField(blank=True, null=True)
    fk_shipping_method = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    extraparams = models.CharField(max_length=255, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_tx = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_supplier_proposal'


class LlxSupplierProposalExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_supplier_proposal_extrafields'


class LlxSupplierProposaldet(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_supplier_proposal = models.ForeignKey(LlxSupplierProposal, models.DO_NOTHING, db_column='fk_supplier_proposal')
    fk_parent_line = models.IntegerField(blank=True, null=True)
    fk_product = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fk_remise_except = models.IntegerField(blank=True, null=True)
    vat_src_code = models.CharField(max_length=10, blank=True, null=True)
    tva_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax1_type = models.CharField(max_length=10, blank=True, null=True)
    localtax2_tx = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)
    localtax2_type = models.CharField(max_length=10, blank=True, null=True)
    qty = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remise_percent = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    remise = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    price = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax1 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_localtax2 = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    info_bits = models.IntegerField(blank=True, null=True)
    buy_price_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_product_fournisseur_price = models.IntegerField(blank=True, null=True)
    special_code = models.IntegerField(blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)
    ref_fourn = models.CharField(max_length=30, blank=True, null=True)
    fk_multicurrency = models.IntegerField(blank=True, null=True)
    multicurrency_code = models.CharField(max_length=3, blank=True, null=True)
    multicurrency_subprice = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ht = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_tva = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    multicurrency_total_ttc = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    fk_unit = models.ForeignKey(LlxCUnits, models.DO_NOTHING, db_column='fk_unit', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_supplier_proposaldet'


class LlxSupplierProposaldetExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_supplier_proposaldet_extrafields'


class LlxTakeposFloorTables(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    label = models.CharField(max_length=255, blank=True, null=True)
    leftpos = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    toppos = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    floor = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_takepos_floor_tables'
        unique_together = (('entity', 'label'),)


class LlxTicket(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=128)
    track_id = models.CharField(unique=True, max_length=128)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_project = models.IntegerField(blank=True, null=True)
    origin_email = models.CharField(max_length=128, blank=True, null=True)
    fk_user_create = models.IntegerField(blank=True, null=True)
    fk_user_assign = models.IntegerField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    fk_statut = models.IntegerField(blank=True, null=True)
    resolution = models.IntegerField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    timing = models.CharField(max_length=20, blank=True, null=True)
    type_code = models.CharField(max_length=32, blank=True, null=True)
    category_code = models.CharField(max_length=32, blank=True, null=True)
    severity_code = models.CharField(max_length=32, blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    date_read = models.DateTimeField(blank=True, null=True)
    date_close = models.DateTimeField(blank=True, null=True)
    notify_tiers_at_create = models.SmallIntegerField(blank=True, null=True)
    email_msgid = models.CharField(max_length=255, blank=True, null=True)
    tms = models.DateTimeField()
    import_key = models.CharField(max_length=14, blank=True, null=True)
    date_last_msg_sent = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_ticket'
        unique_together = (('ref', 'entity'),)


class LlxTicketExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_ticket_extrafields'


class LlxTva(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    datec = models.DateTimeField(blank=True, null=True)
    datep = models.DateField(blank=True, null=True)
    datev = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    fk_typepayment = models.IntegerField(blank=True, null=True)
    num_payment = models.CharField(max_length=50, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    entity = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    paye = models.SmallIntegerField()
    fk_account = models.IntegerField(blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_tva'


class LlxUser(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref_ext = models.CharField(max_length=50, blank=True, null=True)
    admin = models.SmallIntegerField(blank=True, null=True)
    employee = models.SmallIntegerField(blank=True, null=True)
    fk_establishment = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    login = models.CharField(max_length=50)
    pass_encoding = models.CharField(max_length=24, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=128, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    pass_crypted = models.CharField(max_length=128, blank=True, null=True)
    pass_temp = models.CharField(max_length=128, blank=True, null=True)
    api_key = models.CharField(unique=True, max_length=128, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    civility = models.CharField(max_length=6, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=25, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    fk_state = models.IntegerField(blank=True, null=True)
    fk_country = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    job = models.CharField(max_length=128, blank=True, null=True)
    office_phone = models.CharField(max_length=20, blank=True, null=True)
    office_fax = models.CharField(max_length=20, blank=True, null=True)
    user_mobile = models.CharField(max_length=20, blank=True, null=True)
    personal_mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    personal_email = models.CharField(max_length=255, blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    socialnetworks = models.TextField(blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_socpeople = models.IntegerField(unique=True, blank=True, null=True)
    fk_member = models.IntegerField(unique=True, blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    fk_user_expense_validator = models.IntegerField(blank=True, null=True)
    fk_user_holiday_validator = models.IntegerField(blank=True, null=True)
    idpers1 = models.CharField(max_length=128, blank=True, null=True)
    idpers2 = models.CharField(max_length=128, blank=True, null=True)
    idpers3 = models.CharField(max_length=128, blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    datelastlogin = models.DateTimeField(blank=True, null=True)
    datepreviouslogin = models.DateTimeField(blank=True, null=True)
    datelastpassvalidation = models.DateTimeField(blank=True, null=True)
    datestartvalidity = models.DateTimeField(blank=True, null=True)
    dateendvalidity = models.DateTimeField(blank=True, null=True)
    iplastlogin = models.CharField(max_length=250, blank=True, null=True)
    ippreviouslogin = models.CharField(max_length=250, blank=True, null=True)
    egroupware_id = models.IntegerField(blank=True, null=True)
    ldap_sid = models.CharField(max_length=255, blank=True, null=True)
    openid = models.CharField(max_length=255, blank=True, null=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=6, blank=True, null=True)
    color = models.CharField(max_length=6, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    fk_barcode_type = models.IntegerField(blank=True, null=True)
    accountancy_code = models.CharField(max_length=32, blank=True, null=True)
    nb_holiday = models.IntegerField(blank=True, null=True)
    thm = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    tjm = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    salary = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    salaryextra = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    dateemployment = models.DateField(blank=True, null=True)
    dateemploymentend = models.DateField(blank=True, null=True)
    weeklyhours = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    default_range = models.IntegerField(blank=True, null=True)
    default_c_exp_tax_cat = models.IntegerField(blank=True, null=True)
    fk_warehouse = models.IntegerField(blank=True, null=True)
    ref_employee = models.CharField(max_length=50, blank=True, null=True)
    national_registration_number = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_user'
        unique_together = (('login', 'entity'),)
    
    def __str__(self):
        return self.firstname + ' ' + self.lastname


class LlxUserAlert(models.Model):
    rowid = models.AutoField(primary_key=True)
    type = models.IntegerField(blank=True, null=True)
    fk_contact = models.IntegerField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_user_alert'


class LlxUserClicktodial(models.Model):
    fk_user = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=32, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=64, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    poste = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_user_clicktodial'


class LlxUserEmployment(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    ref = models.CharField(max_length=50, blank=True, null=True)
    ref_ext = models.CharField(max_length=50, blank=True, null=True)
    fk_user = models.ForeignKey(LlxUser, models.DO_NOTHING, db_column='fk_user', blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    job = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField()
    salary = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    salaryextra = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    weeklyhours = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    dateemployment = models.DateField(blank=True, null=True)
    dateemploymentend = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_user_employment'
        unique_together = (('ref', 'entity'),)


class LlxUserExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_user_extrafields'


class LlxUserHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    rowid = models.IntegerField(blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    ref_ext = models.CharField(max_length=50, blank=True, null=True)
    ref_int = models.CharField(max_length=50, blank=True, null=True)
    admin = models.SmallIntegerField(blank=True, null=True)
    employee = models.SmallIntegerField(blank=True, null=True)
    fk_establishment = models.IntegerField(blank=True, null=True)
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField(blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    login = models.CharField(max_length=50, blank=True, null=True)
    pass_encoding = models.CharField(max_length=24, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=128, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    pass_crypted = models.CharField(max_length=128, blank=True, null=True)
    pass_temp = models.CharField(max_length=128, blank=True, null=True)
    api_key = models.CharField(max_length=128, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    civility = models.CharField(max_length=6, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=25, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    fk_state = models.IntegerField(blank=True, null=True)
    fk_country = models.IntegerField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    job = models.CharField(max_length=128, blank=True, null=True)
    office_phone = models.CharField(max_length=20, blank=True, null=True)
    office_fax = models.CharField(max_length=20, blank=True, null=True)
    user_mobile = models.CharField(max_length=20, blank=True, null=True)
    personal_mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    personal_email = models.CharField(max_length=255, blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    socialnetworks = models.TextField(blank=True, null=True)
    fk_soc = models.IntegerField(blank=True, null=True)
    fk_socpeople = models.IntegerField(blank=True, null=True)
    fk_member = models.IntegerField(blank=True, null=True)
    fk_user = models.IntegerField(blank=True, null=True)
    fk_user_expense_validator = models.IntegerField(blank=True, null=True)
    fk_user_holiday_validator = models.IntegerField(blank=True, null=True)
    idpers1 = models.CharField(max_length=128, blank=True, null=True)
    idpers2 = models.CharField(max_length=128, blank=True, null=True)
    idpers3 = models.CharField(max_length=128, blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)
    datelastlogin = models.DateTimeField(blank=True, null=True)
    datepreviouslogin = models.DateTimeField(blank=True, null=True)
    datelastpassvalidation = models.DateTimeField(blank=True, null=True)
    datestartvalidity = models.DateTimeField(blank=True, null=True)
    dateendvalidity = models.DateTimeField(blank=True, null=True)
    iplastlogin = models.CharField(max_length=250, blank=True, null=True)
    ippreviouslogin = models.CharField(max_length=250, blank=True, null=True)
    egroupware_id = models.IntegerField(blank=True, null=True)
    ldap_sid = models.CharField(max_length=255, blank=True, null=True)
    openid = models.CharField(max_length=255, blank=True, null=True)
    statut = models.SmallIntegerField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=6, blank=True, null=True)
    color = models.CharField(max_length=6, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    fk_barcode_type = models.IntegerField(blank=True, null=True)
    accountancy_code = models.CharField(max_length=32, blank=True, null=True)
    nb_holiday = models.IntegerField(blank=True, null=True)
    thm = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    tjm = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    salary = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    salaryextra = models.DecimalField(max_digits=24, decimal_places=8, blank=True, null=True)
    dateemployment = models.DateField(blank=True, null=True)
    dateemploymentend = models.DateField(blank=True, null=True)
    weeklyhours = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    default_range = models.IntegerField(blank=True, null=True)
    default_c_exp_tax_cat = models.IntegerField(blank=True, null=True)
    fk_warehouse = models.IntegerField(blank=True, null=True)
    operation_type = models.CharField(max_length=10, blank=True, null=True)
    operation_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_user_history'


class LlxUserParam(models.Model):
    fk_user = models.IntegerField()
    entity = models.IntegerField()
    param = models.CharField(max_length=180)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'llx_user_param'
        unique_together = (('fk_user', 'param', 'entity'),)


class LlxUserRib(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_user = models.IntegerField()
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    label = models.CharField(max_length=30, blank=True, null=True)
    bank = models.CharField(max_length=255, blank=True, null=True)
    code_banque = models.CharField(max_length=128, blank=True, null=True)
    code_guichet = models.CharField(max_length=6, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    cle_rib = models.CharField(max_length=5, blank=True, null=True)
    bic = models.CharField(max_length=11, blank=True, null=True)
    iban_prefix = models.CharField(max_length=34, blank=True, null=True)
    domiciliation = models.CharField(max_length=255, blank=True, null=True)
    proprio = models.CharField(max_length=60, blank=True, null=True)
    owner_address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_user_rib'


class LlxUserRights(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    fk_user = models.ForeignKey(LlxUser, models.DO_NOTHING, db_column='fk_user')
    fk_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_user_rights'
        unique_together = (('entity', 'fk_user', 'fk_id'),)


class LlxUsergroup(models.Model):
    rowid = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=180)
    entity = models.IntegerField()
    datec = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    model_pdf = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_usergroup'
        unique_together = (('nom', 'entity'),)


class LlxUsergroupExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_usergroup_extrafields'


class LlxUsergroupRights(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    fk_usergroup = models.ForeignKey(LlxUsergroup, models.DO_NOTHING, db_column='fk_usergroup')
    fk_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'llx_usergroup_rights'
        unique_together = (('entity', 'fk_usergroup', 'fk_id'),)


class LlxUsergroupUser(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    fk_user = models.ForeignKey(LlxUser, models.DO_NOTHING, db_column='fk_user')
    fk_usergroup = models.ForeignKey(LlxUsergroup, models.DO_NOTHING, db_column='fk_usergroup')

    class Meta:
        managed = False
        db_table = 'llx_usergroup_user'
        unique_together = (('entity', 'fk_user', 'fk_usergroup'),)


class LlxWebsite(models.Model):
    rowid = models.AutoField(primary_key=True)
    type_container = models.CharField(max_length=16)
    entity = models.IntegerField()
    ref = models.CharField(max_length=128)
    description = models.CharField(max_length=255, blank=True, null=True)
    maincolor = models.CharField(max_length=16, blank=True, null=True)
    maincolorbis = models.CharField(max_length=16, blank=True, null=True)
    lang = models.CharField(max_length=8, blank=True, null=True)
    otherlang = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    fk_default_home = models.IntegerField(blank=True, null=True)
    use_manifest = models.IntegerField(blank=True, null=True)
    virtualhost = models.CharField(max_length=255, blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    lastaccess = models.DateTimeField(blank=True, null=True)
    pageviews_month = models.BigIntegerField(blank=True, null=True)
    pageviews_total = models.BigIntegerField(blank=True, null=True)
    tms = models.DateTimeField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_website'
        unique_together = (('ref', 'entity'),)


class LlxWebsiteExtrafields(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_object = models.IntegerField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_website_extrafields'


class LlxWebsitePage(models.Model):
    rowid = models.AutoField(primary_key=True)
    fk_website = models.ForeignKey(LlxWebsite, models.DO_NOTHING, db_column='fk_website')
    type_container = models.CharField(max_length=16)
    pageurl = models.CharField(max_length=255)
    aliasalt = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    lang = models.CharField(max_length=6, blank=True, null=True)
    fk_page = models.IntegerField(blank=True, null=True)
    allowed_in_frames = models.IntegerField(blank=True, null=True)
    htmlheader = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    grabbed_from = models.CharField(max_length=255, blank=True, null=True)
    fk_user_creat = models.IntegerField(blank=True, null=True)
    fk_user_modif = models.IntegerField(blank=True, null=True)
    author_alias = models.CharField(max_length=64, blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    import_key = models.CharField(max_length=14, blank=True, null=True)
    object_type = models.CharField(max_length=255, blank=True, null=True)
    fk_object = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_website_page'
        unique_together = (('fk_website', 'pageurl'),)


class LlxWorkstationWorkstation(models.Model):
    rowid = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=128)
    label = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=7, blank=True, null=True)
    note_public = models.TextField(blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    note_private = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    tms = models.DateTimeField()
    fk_user_creat = models.ForeignKey(LlxUser, models.DO_NOTHING, db_column='fk_user_creat')
    fk_user_modif = models.IntegerField(blank=True, null=True)
    import_key = models.CharField(max_length=14, blank=True, null=True)
    status = models.SmallIntegerField()
    nb_operators_required = models.IntegerField(blank=True, null=True)
    thm_operator_estimated = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    thm_machine_estimated = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_workstation_workstation'


class LlxWorkstationWorkstationResource(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_resource = models.IntegerField(blank=True, null=True)
    fk_workstation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_workstation_workstation_resource'


class LlxWorkstationWorkstationUsergroup(models.Model):
    rowid = models.AutoField(primary_key=True)
    tms = models.DateTimeField()
    fk_usergroup = models.IntegerField(blank=True, null=True)
    fk_workstation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_workstation_workstation_usergroup'


class LlxZapierHook(models.Model):
    rowid = models.AutoField(primary_key=True)
    entity = models.IntegerField()
    url = models.CharField(max_length=255, blank=True, null=True)
    event = models.CharField(max_length=255, blank=True, null=True)
    module = models.CharField(max_length=128, blank=True, null=True)
    action = models.CharField(max_length=128, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    date_creation = models.DateTimeField(blank=True, null=True)
    fk_user = models.IntegerField()
    tms = models.DateTimeField()
    import_key = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'llx_zapier_hook'
