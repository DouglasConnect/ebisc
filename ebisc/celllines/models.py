from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist


class Gender(models.Model):

    name = models.CharField(_(u'Gender'), max_length=10, unique=True)

    class Meta:
        verbose_name = _(u'Gender')
        verbose_name_plural = _(u'Genders')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class AgeRange(models.Model):

    name = models.CharField(_(u'Age range'), max_length=10, unique=True)

    class Meta:
        verbose_name = _(u'Age range')
        verbose_name_plural = _(u'Age ranges')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class Accesslevel(models.Model):
    accesslevel = models.CharField(_(u'Access level'), max_length=20, blank=True)

    class Meta:
        verbose_name = _(u'Access level')
        verbose_name_plural = _(u'Access levels')
        ordering = ['accesslevel']

    def __unicode__(self):
        return u'%s' % (self.accesslevel,)


class Aliquotstatus(models.Model):
    aliquotstatus = models.CharField(_(u'Aliquot status'), max_length=20, blank=True)

    class Meta:
        verbose_name = _(u'Aliquot status')
        verbose_name_plural = _(u'Aliquot statuses')
        ordering = ['aliquotstatus']

    def __unicode__(self):
        return u'%s' % (self.aliquotstatus,)


class Approveduse(models.Model):
    approveduse = models.CharField(_(u'Approved use'), max_length=60, blank=True)

    class Meta:
        verbose_name = _(u'Approved use')
        verbose_name_plural = _(u'Approved uses')
        ordering = ['approveduse']

    def __unicode__(self):
        return u'%s' % (self.approveduse,)


class Batchstatus(models.Model):
    batchstatus = models.CharField(_(u'Batch status'), max_length=20, blank=True)

    class Meta:
        verbose_name = _(u'Batch status')
        verbose_name_plural = _(u'Batch statuses')
        ordering = ['batchstatus']

    def __unicode__(self):
        return u'%s' % (self.batchstatus,)


class Binnedage(models.Model):
    binnedage = models.CharField(_(u'Binned age'), max_length=5, blank=True)

    class Meta:
        verbose_name = _(u'Binned age')
        verbose_name_plural = _(u'Binned ages')
        ordering = ['id']

    def __unicode__(self):
        return u'%s' % (self.binnedage,)


class Cellline(models.Model):

    ACCEPTED_CHOICES = (
        ('pending', _(u'Pending')),
        ('accepted', _(u'Accepted')),
        ('rejected', _(u'Rejected')),
    )

    celllineaccepted = models.CharField(_(u'Cell line accepted'), max_length=10, choices=ACCEPTED_CHOICES, default='pending')

    biosamplesid = models.CharField(_(u'Biosamples ID'), unique=True, max_length=12)
    celllinename = models.CharField(_(u'Cell line name'), unique=True, max_length=15)

    donor = models.ForeignKey('Donor', verbose_name=_(u'Donor'), blank=True, null=True)
    donor_age = models.ForeignKey(AgeRange, verbose_name=_(u'Age'), blank=True, null=True)

    generator = models.ForeignKey('Organization', verbose_name=_(u'Generator'), related_name='generator_of_cell_lines')
    owner = models.ForeignKey('Organization', verbose_name=_(u'Owner'), null=True, blank=True, related_name='owner_of_cell_lines')

    celllineprimarydisease = models.ForeignKey('Disease', verbose_name=_(u'Disease'), blank=True, null=True)
    celllinediseaseaddinfo = models.CharField(_(u'Cell line disease info'), max_length=100, null=True, blank=True)
    celllinestatus = models.ForeignKey('Celllinestatus', verbose_name=_(u'Cell line status'), blank=True, null=True)
    celllinecelltype = models.ForeignKey('Celltype', verbose_name=_(u'Cell type'), blank=True, null=True)
    celllinecollection = models.ForeignKey('Celllinecollection', verbose_name=_(u'Cell line collection'), blank=True, null=True)
    celllinetissuesource = models.ForeignKey('Tissuesource', verbose_name=_(u'Tissue source'), blank=True, null=True)
    celllinetissuetreatment = models.ForeignKey('Clinicaltreatmentb4donation', verbose_name=_(u'Clinical treatment B4 donation'), blank=True, null=True)
    celllinetissuedate = models.DateField(_(u'Cell line tissue date'), blank=True, null=True)
    celllinenamesynonyms = models.CharField(_(u'Cell line name synonyms'), max_length=500, null=True, blank=True)
    depositorscelllineuri = models.CharField(_(u'Depositors cell line URI'), max_length=45, blank=True)
    celllinecomments = models.TextField(_(u'Cell line comments'), null=True, blank=True)
    celllineecaccurl = models.URLField(_(u'Cell line ECACC URL'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line')
        verbose_name_plural = _(u'Cell lines')
        ordering = ['biosamplesid']

    def __unicode__(self):
        return u'%s' % (self.biosamplesid,)

    def to_elastic(self):

        try:
            disease = self.celllineprimarydisease and self.celllineprimarydisease.disease or None
            disease_synonyms = self.celllineprimarydisease and [s.strip() for s in self.celllineprimarydisease.synonyms.split(',')] or None
        except ObjectDoesNotExist:
            disease = None
            disease_synonyms = None

        return {
            'biosamplesid': self.biosamplesid,
            'celllinename': self.celllinename,
            'celllineprimarydisease': disease,
            'celllineprimarydisease_synonyms': disease_synonyms,
            'depositor': self.generator.organizationname,
            'celllinecelltype': self.celllinecelltype.celltype,
            'celllinenamesynonyms': self.celllinenamesynonyms,
        }


class Celllinealiquot(models.Model):
    aliquotcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    aliquotstatus = models.ForeignKey('Aliquotstatus', verbose_name=_(u'Aliquot status'), blank=True, null=True)
    aliquotstatusdate = models.CharField(_(u'Aliquot status date'), max_length=20, blank=True)
    aliquotupdatedby = models.ForeignKey('Useraccount', verbose_name=_(u'User account'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line aliquot')
        verbose_name_plural = _(u'Cell line aliquotes')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllineannotation(models.Model):
    annotationcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    celllineannotationsource = models.CharField(_(u'Cell line annotation source'), max_length=45, blank=True)
    celllineannotationsourceid = models.CharField(_(u'Cell line annotation source id'), max_length=45, blank=True)
    celllineannotationsourceversion = models.CharField(_(u'Cell line annotation source version'), max_length=45, blank=True)
    celllineannotation = models.TextField(_(u'Cell line annotation'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Cell line annotation')
        verbose_name_plural = _(u'Cell line annotations')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinebatch(models.Model):
    batchcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    batchstatus = models.ForeignKey('Batchstatus', verbose_name=_(u'Batch status'), blank=True, null=True)
    batchstatusdate = models.CharField(_(u'Batch status date'), max_length=20, blank=True)
    batchstatusupdatedby = models.ForeignKey('Useraccount', verbose_name=_(u'User account'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line batch')
        verbose_name_plural = _(u'Cell line batches')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinecharacterization(models.Model):
    characterizationcellline = models.OneToOneField(Cellline, verbose_name=_(u'Cell line'), blank=True, null=True)
    certificateofanalysispassage = models.CharField(_(u'Certificate of analysis passage'), max_length=5, blank=True)
    hiv1screening = models.IntegerField(_(u'Hiv1 screening'), blank=True, null=True)
    hiv2screening = models.IntegerField(_(u'Hiv2 screening'), blank=True, null=True)
    hepititusb = models.IntegerField(_(u'Hepititus b'), blank=True, null=True)
    hepititusc = models.IntegerField(_(u'Hepititus c'), blank=True, null=True)
    mycoplasma = models.IntegerField(_(u'Mycoplasma'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line characterization')
        verbose_name_plural = _(u'Cell line characterizations')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinechecklist(models.Model):
    checklistcellline = models.OneToOneField(Cellline, verbose_name=_(u'Cell line'))
    morphologicalassessment = models.BooleanField(_(u'Morphological assessment'), default=False)
    facs = models.BooleanField(_(u'FACS'), default=False)
    ihc = models.BooleanField(_(u'IHC'), default=False)
    pcrforreprofactorremoval = models.BooleanField(_(u'PCR for reprofactor removal'), default=False)
    pcrforpluripotency = models.BooleanField(_(u'PCR for pluripotency'), default=False)
    teratoma = models.BooleanField(_(u'Teratoma'), default=False)
    invitrodifferentiation = models.BooleanField(_(u'Invitro differentiation'), default=False)
    karyotype = models.BooleanField(_(u'Karyo type'), default=False)
    cnvanalysis = models.BooleanField(_(u'CNV analysis'), default=False)
    dnamethylation = models.BooleanField(_(u'DNA methylation'), default=False)
    microbiologyinclmycoplasma = models.BooleanField(_(u'Micro biology inclmycoplasma'), default=False)
    dnagenotyping = models.BooleanField(_(u'DNA genotyping'), default=False)
    hlatyping = models.BooleanField(_(u'HLA typing'), default=False)
    virustesting = models.BooleanField(_(u'Virus testing'), default=False)
    postthawviability = models.BooleanField(_(u'Post thawviability'), default=False)
    checklistcomments = models.TextField('Checklist comments', null=True, blank=True)

    class Meta:
        verbose_name = _(u'Cell line checklist')
        verbose_name_plural = _(u'Cell line checklists')
        ordering = ['checklistcellline']

    def __unicode__(self):
        return u'%s' % (self.checklistcellline,)


class Celllinecollection(models.Model):
    celllinecollectiontotal = models.IntegerField(_(u'Cell line collection total'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line collection')
        verbose_name_plural = _(u'Cell line collections')
        ordering = ['id']

    def __unicode__(self):
        return u'%s' % (self.celllinecollectiontotal,)


class Celllinecomments(models.Model):
    commentscellline = models.IntegerField(_(u'Comments cell line'), blank=True, null=True)
    celllinecomments = models.TextField(blank=True)

    class Meta:
        verbose_name = _(u'Cell line comments')
        verbose_name_plural = _(u'Cell line comments')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinecultureconditions(models.Model):

    cell_line = models.OneToOneField(Cellline, verbose_name=_(u'Cell line'))

    surfacecoating = models.ForeignKey('SurfaceCoating', verbose_name=_(u'Surface coating'), null=True, blank=True)
    feedercelltype = models.CharField(_(u'Feeder cell type'), max_length=45, null=True, blank=True)
    feedercellid = models.CharField(_(u'Feeder cell id'), max_length=45, null=True, blank=True)
    passagemethod = models.ForeignKey('PassageMethod', verbose_name=_(u'Passage method'), blank=True, null=True)
    enzymatically = models.ForeignKey('Enzymatically', verbose_name=_(u'Enzymatically'), blank=True, null=True)
    enzymefree = models.ForeignKey('EnzymeFree', verbose_name=_(u'Enzyme free'), blank=True, null=True)
    o2concentration = models.IntegerField(_(u'O2 concentration'), blank=True, null=True)
    co2concentration = models.IntegerField(_(u'Co2 concentration'), blank=True, null=True)

    culture_medium = models.ForeignKey('CultureMedium', verbose_name=_(u'Culture medium'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line culture conditions')
        verbose_name_plural = _(u'Cell line culture conditions')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class CultureMedium(models.Model):
    name = models.CharField(_(u'Culture medium'), max_length=45, unique=True)

    class Meta:
        verbose_name = _(u'Culture medium')
        verbose_name_plural = _(u'Culture mediums')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class CultureMediumOther(models.Model):
    cell_line_culture_conditions = models.OneToOneField(Celllinecultureconditions, verbose_name=_(u'Cell line culture conditions'), related_name='culture_medium_other')

    base = models.CharField(_(u'Culture medium base'), max_length=45, blank=True)
    protein_source = models.ForeignKey('ProteinSource', verbose_name=_(u'Protein source'), blank=True, null=True)
    serum_concentration = models.IntegerField(_(u'Serum concentration'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Culture medium')
        verbose_name_plural = _(u'Culture mediums')
        ordering = ['base', 'protein_source', 'serum_concentration']

    def __unicode__(self):
        return u'%s / %s / %s' % (self.base, self.protein_source, self.serum_concentration)


class CellLineCultureMediumSupplement(models.Model):
    cell_line_culture_conditions = models.ForeignKey(Celllinecultureconditions, verbose_name=_(u'Cell line culture conditions'), related_name='medium_supplements')

    supplement = models.CharField(_(u'Supplement'), max_length=45)
    amount = models.CharField(_(u'Amount'), max_length=45, null=True, blank=True)
    unit = models.ForeignKey('Unit', verbose_name=_(u'Unit'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Cell line culture supplements')
        verbose_name_plural = _(u'Cell line culture supplements')
        ordering = ['supplement']

    def __unicode__(self):
        if self.amount and self.unit:
            return '%s - %s %s' % (self.supplement, self.amount, self.unit)
        else:
            return unicode(self.supplement)


class Celllinederivation(models.Model):

    cell_line = models.OneToOneField(Cellline, verbose_name=_(u'Cell line'), blank=True, null=True)

    primarycelltypename = models.CharField(_(u'Primary cell type name'), max_length=45, blank=True)
    primarycelltypecellfinderid = models.CharField(_(u'Primary cell type cell finder id'), max_length=45, blank=True)
    primarycelldevelopmentalstage = models.ForeignKey('PrimaryCellDevelopmentalStage', verbose_name=_(u'Primary cell developmental stage'), blank=True, null=True)
    selectioncriteriaforclones = models.TextField(_(u'Selection criteria for clones'), null=True, blank=True)
    xenofreeconditions = models.NullBooleanField(_(u'Xeno free conditions'), default=None, null=True, blank=True)
    derivedundergmp = models.NullBooleanField(_(u'Derived under gmp'), default=None, null=True, blank=True)
    availableasclinicalgrade = models.CharField(_(u'Available as clinical grade'), max_length=4, blank=True)

    class Meta:
        verbose_name = _(u'Cell line derivation')
        verbose_name_plural = _(u'Cell line derivations')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinediffpotency(models.Model):
    diffpotencycellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    passagenumber = models.CharField(_(u'Passage number'), max_length=5, blank=True)
    germlayer = models.ForeignKey('Germlayer', verbose_name=_(u'Germlayer'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line diff potency')
        verbose_name_plural = _(u'Cell line diff potencies')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinediffpotencymarker(models.Model):
    celllinediffpotency = models.ForeignKey('Celllinediffpotency', verbose_name=_(u'Cell line diff potency'), blank=True, null=True)
    morphologymethod = models.ForeignKey('Morphologymethod', verbose_name=_(u'Morphology method'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line diff potency marker')
        verbose_name_plural = _(u'Cell line diff potency markers')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinediffpotencymolecule(models.Model):
    celllinediffpotencymarker = models.IntegerField(_(u'Cell line diff potency marker'), blank=True, null=True)
    diffpotencymolecule = models.ForeignKey('Molecule', verbose_name=_(u'Molecule'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line diff potency molecule')
        verbose_name_plural = _(u'Cell line diff potency molecules')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinegenemutations(models.Model):
    genemutationscellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    weblink = models.CharField(_(u'Weblink'), max_length=100, blank=True)

    class Meta:
        verbose_name = _(u'Cell line gene mutations')
        verbose_name_plural = _(u'Cell line gene mutations')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinegenemutationsmolecule(models.Model):
    celllinegenemutations = models.ForeignKey('Celllinegenemutations', verbose_name=_(u'Cell line gene mutations'), blank=True, null=True)
    genemutationsmolecule = models.ForeignKey('Molecule', verbose_name=_(u'Molecule'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line gene mutations molecule')
        verbose_name_plural = _(u'Cell line gene mutations molecules')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinegeneticmod(models.Model):
    geneticmodcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    celllinegeneticmod = models.CharField(_(u'Cell line genetic mod'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Cell line genetic mod')
        verbose_name_plural = _(u'Cell line genetic modes')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinegenomeseq(models.Model):
    genomeseqcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    celllinegenomeseqlink = models.CharField(_(u'Cell line genome seq link'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Cell line genome seqence')
        verbose_name_plural = _(u'Cell line genome seqences')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinegenotypingother(models.Model):
    genometypothercellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    celllinegenotypingother = models.TextField(_(u'Cell line geno typing other'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Cell line genotyping other')
        verbose_name_plural = _(u'Cell line genotyping others')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinehlatyping(models.Model):
    hlatypingcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    celllinehlaclass = models.IntegerField(_(u'Cell line hla class'), blank=True, null=True)
    celllinehla = models.ForeignKey('Hla', verbose_name=_(u'Hla'), blank=True, null=True)
    celllinehlaallele1 = models.CharField(_(u'Cell line hla all ele1'), max_length=45, blank=True)
    celllinehlaallele2 = models.CharField(_(u'Cell line hla all ele2'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Cell line hla typing')
        verbose_name_plural = _(u'Cell line hla typing')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class CellLineKaryotype(models.Model):

    cell_line = models.OneToOneField('Cellline', verbose_name=_(u'Cell line'), related_name='karyotype')

    karyotype = models.CharField(_(u'Karyotype'), max_length=500, null=True, blank=True)
    karyotype_method = models.ForeignKey('KaryotypeMethod', verbose_name=_(u'Karyotype method'), null=True, blank=True)

    passage_number = models.IntegerField(_(u'Passage number'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Cell line karyotype')
        verbose_name_plural = _(u'Cell line karyotypes')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinelab(models.Model):
    labcellline = models.OneToOneField(Cellline, verbose_name=_(u'Cell line'), blank=True, null=True)
    cryodate = models.DateField(blank=True, null=True)
    expansioninprogress = models.IntegerField(_(u'Expansion in progress'), blank=True, null=True)
    funder = models.CharField(_(u'Funder'), max_length=45, blank=True)
    mutagene = models.CharField(_(u'Mutagene'), max_length=100, blank=True)
    reprogrammingmethod1 = models.ForeignKey('Reprogrammingmethod1', verbose_name=_(u'Reprogramming method 1'), blank=True, null=True)
    reprogrammingmethod2 = models.ForeignKey('Reprogrammingmethod2', verbose_name=_(u'Reprogramming method 2'), blank=True, null=True)
    reprogrammingmethod3 = models.ForeignKey('Reprogrammingmethod3', verbose_name=_(u'Reprogramming method 3'), blank=True, null=True)
    clonenumber = models.IntegerField(_(u'Clone number'), blank=True, null=True)
    passagenumber = models.CharField(_(u'Passage number'), max_length=5, blank=True)
    culturesystem = models.ForeignKey('Culturesystem', verbose_name=_(u'Culture system'), blank=True, null=True)
    culturesystemcomment = models.CharField(_(u'Culture system comment'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Cell line lab')
        verbose_name_plural = _(u'Cell line labs')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class CellLineLegal(models.Model):

    cell_line = models.OneToOneField(Cellline, verbose_name=_(u'Cell line'))

    q1donorconsent = models.NullBooleanField(_(u'Q1 donor consent'), default=None, blank=True, null=True)
    q2donortrace = models.IntegerField(_(u'Q2 donor trace'), blank=True, null=True)
    q3irbapproval = models.IntegerField(_(u'Q3 irb approval'), blank=True, null=True)
    q4approveduse = models.ForeignKey('Approveduse', verbose_name=_(u'Approved use'), blank=True, null=True)
    q5informedconsentreference = models.CharField(_(u'Q5 informed consent reference'), max_length=20, blank=True)
    q6restrictions = models.TextField(_(u'Q6 restrictions'), null=True, blank=True)
    q7iprestrictions = models.TextField(_(u'Q7 ip restrictions'), null=True, blank=True)
    q8jurisdiction = models.ForeignKey('Country', verbose_name=_(u'Country'), blank=True, null=True)
    q9applicablelegislationandregulation = models.TextField(_(u'Q9 applicable legislation and regulation'), null=True, blank=True)
    q10managedaccess = models.TextField(_(u'Q10 managed access'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Cell line legal')
        verbose_name_plural = _(u'Cell line legal')

    def __unicode__(self):
        return u'%s' % (self.cell_line,)


class Celllinemarker(models.Model):
    markercellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), unique=True)
    morphologymethod = models.ForeignKey('Morphologymethod', verbose_name=_(u'Morphology method'), blank=True, null=True)
    celllinemarker = models.ForeignKey('Marker', verbose_name=_(u'Marker'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line marker')
        verbose_name_plural = _(u'Cell line markers')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllineorganization(models.Model):
    orgcellline = models.ForeignKey(Cellline, verbose_name=_(u'Cell line'), related_name='organizations')
    organization = models.ForeignKey('Organization', verbose_name=_(u'Organization'))
    celllineorgtype = models.ForeignKey('Celllineorgtype', verbose_name=_(u'Cell line org type'))
    orgstatus = models.IntegerField(_(u'Org status'), blank=True, null=True)
    orgregistrationdate = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line organization')
        verbose_name_plural = _(u'Cell line organizations')
        unique_together = ('orgcellline', 'organization', 'celllineorgtype')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllineorgtype(models.Model):
    celllineorgtype = models.CharField(_(u'Cell line org type'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Cell line org type')
        verbose_name_plural = _(u'Cell line org types')
        ordering = ['celllineorgtype']

    def __unicode__(self):
        return u'%s' % (self.celllineorgtype,)


class Celllinepublication(models.Model):
    publicationcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    pubmedreference = models.CharField(_(u'Pubmed reference'), max_length=45, blank=True)
    celllinepublicationdoiurl = models.URLField(_(u'Cell line publication doi url'), blank=True, null=True)
    celllinepublisher = models.ForeignKey('Publisher', verbose_name=_(u'Publisher'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line publication')
        verbose_name_plural = _(u'Cell line publications')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinesnp(models.Model):
    snpcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    weblink = models.CharField(_(u'Weblink'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Cell line snp')
        verbose_name_plural = _(u'Cell line snps')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinesnpdetails(models.Model):
    celllinesnp = models.ForeignKey('Celllinesnp', verbose_name=_(u'Cell line snp'), blank=True, null=True)
    celllinesnpgene = models.CharField(_(u'Cell line snp gene'), max_length=45, blank=True)
    celllinesnpchromosomalposition = models.CharField(_(u'Cell line snp chromosomal position'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Cell line snp details')
        verbose_name_plural = _(u'Cell line snp details')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinesnprslinks(models.Model):
    celllinesnp = models.ForeignKey('Celllinesnp', verbose_name=_(u'Cel lline snp'), blank=True, null=True)
    rsnumber = models.CharField(_(u'Rs number'), max_length=45, blank=True)
    rslink = models.CharField(_(u'Rs link'), max_length=100, blank=True)

    class Meta:
        verbose_name = _(u'Cell line snp Rs links')
        verbose_name_plural = _(u'Cell line snp Rs links')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinestatus(models.Model):
    celllinestatus = models.CharField(_(u'Cell line status'), max_length=50, blank=True)

    class Meta:
        verbose_name = _(u'Cell line status')
        verbose_name_plural = _(u'Cell line statuses')
        ordering = ['celllinestatus']

    def __unicode__(self):
        return u'%s' % (self.celllinestatus,)


class Celllinestrfingerprinting(models.Model):
    strfpcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    locus = models.ForeignKey('Strfplocus', verbose_name=_(u'STR fplocus'), blank=True, null=True)
    allele1 = models.CharField(_(u'All ele1'), max_length=45, blank=True)
    allele2 = models.CharField(_(u'All ele2'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Cell line STR finger printing')
        verbose_name_plural = _(u'Cell line STR finger printings')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celllinevalue(models.Model):
    valuecellline = models.OneToOneField(Cellline, verbose_name=_(u'Cell line'), blank=True, null=True)
    potentialuse = models.CharField(_(u'Potential use'), max_length=100, blank=True)
    valuetosociety = models.CharField(_(u'Value to society'), max_length=100, blank=True)
    valuetoresearch = models.CharField(_(u'Value to research'), max_length=100, blank=True)
    othervalue = models.CharField(_(u'Other value'), max_length=100, blank=True)

    class Meta:
        verbose_name = _(u'Cell line value')
        verbose_name_plural = _(u'Cell line values')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Celltype(models.Model):
    celltype = models.CharField(_(u'Celltype'), max_length=100, blank=True)

    class Meta:
        verbose_name = _(u'Cell type')
        verbose_name_plural = _(u'Cell types')
        ordering = ['celltype']

    def __unicode__(self):
        return u'%s' % (self.celltype,)


class Clinicaltreatmentb4donation(models.Model):
    clinicaltreatmentb4donation = models.CharField(_(u'Clininical treatment b4 donation'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Clininical treatment B4 donation')
        verbose_name_plural = _(u'Clininical treatment B4 donations')
        ordering = ['clinicaltreatmentb4donation']

    def __unicode__(self):
        return u'%s' % (self.clinicaltreatmentb4donation,)


class Contact(models.Model):
    contacttype = models.ForeignKey('Contacttype', verbose_name=_(u'Contact type'), blank=True, null=True)
    country = models.ForeignKey('Country', verbose_name=_(u'Country'), db_column='country')
    postcode = models.ForeignKey('Postcode', verbose_name=_(u'Postcode'), db_column='postcode')
    statecounty = models.IntegerField(_(u'State county'), blank=True, null=True)
    city = models.CharField(_(u'City'), max_length=45, blank=True)
    street = models.CharField(_(u'Street'), max_length=45, blank=True)
    buildingnumber = models.CharField(_(u'Building number'), max_length=20, blank=True)
    suiteoraptordept = models.CharField(_(u'Suite or apt or dept'), max_length=10, null=True, blank=True)
    officephonecountrycode = models.ForeignKey('Phonecountrycode', verbose_name=_(u'Phone country code'), related_name='contacts_officephonecountrycode', blank=True, null=True)
    officephone = models.CharField(_(u'Office phone'), max_length=20, null=True, blank=True)
    faxcountrycode = models.ForeignKey('Phonecountrycode', verbose_name=_(u'Phone country code'), related_name='contacts_faxcountrycode', blank=True, null=True)
    fax = models.CharField(_(u'Fax'), max_length=20, null=True, blank=True)
    mobilecountrycode = models.ForeignKey('Phonecountrycode', verbose_name=_(u'Phone country code'), related_name='contacts_mobilecountrycode', blank=True, null=True)
    mobilephone = models.CharField(_(u'Mobile phone'), max_length=20, null=True, blank=True)
    website = models.CharField(_(u'Website'), max_length=45, null=True, blank=True)
    emailaddress = models.CharField(_(u'Email address'), max_length=45, null=True, blank=True)

    class Meta:
        verbose_name = _(u'Contact')
        verbose_name_plural = _(u'Contacts')
        ordering = []

    def __unicode__(self):
        return u'%s' % (self.id,)


class Contacttype(models.Model):
    contacttype = models.CharField(_(u'Contact type'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Contact type')
        verbose_name_plural = _(u'Contact types')
        ordering = ['contacttype']

    def __unicode__(self):
        return u'%s' % (self.contacttype,)


class Country(models.Model):
    country = models.CharField(_(u'Country'), max_length=45, unique=True)
    countrycode = models.CharField(_(u'Country code'), max_length=3, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = _(u'Country')
        verbose_name_plural = _(u'Countries')
        ordering = ['country']

    def __unicode__(self):
        return u'%s' % (self.country,)


class Culturesystem(models.Model):
    culturesystem = models.CharField(_(u'Culture system'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Culture system')
        verbose_name_plural = _(u'Culture systems')
        ordering = ['culturesystem']

    def __unicode__(self):
        return u'%s' % (self.culturesystem,)


class Disease(models.Model):
    icdcode = models.CharField(_(u'DOID'), max_length=30, unique=True, null=True, blank=True)
    disease = models.CharField(_(u'Disease'), max_length=45, blank=True)
    synonyms = models.CharField(_(u'Synonyms'), max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = _(u'Disease')
        verbose_name_plural = _(u'Diseases')
        ordering = ['disease']

    def __unicode__(self):
        return u'%s' % (self.disease,)


class Document(models.Model):
    cellline = models.IntegerField(_(u'Cell line'), blank=True, null=True)
    title = models.CharField(_(u'Title'), max_length=45, blank=True)
    abstract = models.TextField(_(u'Abstract'), null=True, blank=True)
    documenttype = models.ForeignKey('Documenttype', verbose_name=_(u'Document type'), blank=True, null=True)
    documentdepositor = models.IntegerField(_(u'Document depositor'), blank=True, null=True)
    authors = models.TextField(_(u'Authors'), null=True, blank=True)
    owner = models.IntegerField(_(u'Owner'), blank=True, null=True)
    version = models.CharField(_(u'Version'), max_length=5, blank=True)
    accesslevel = models.IntegerField(_(u'Access level'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Document')
        verbose_name_plural = _(u'Documents')
        ordering = ['title']

    def __unicode__(self):
        return u'%s' % (self.title,)


class Documenttype(models.Model):
    documenttype = models.CharField(_(u'Document type'), max_length=30, blank=True)

    class Meta:
        verbose_name = _(u'Document type')
        verbose_name_plural = _(u'Document types')
        ordering = ['documenttype']

    def __unicode__(self):
        return u'%s' % (self.documenttype,)


class Donor(models.Model):

    biosamplesid = models.CharField(_(u'Biosamples ID'), max_length=12, unique=True)
    gender = models.ForeignKey(Gender, verbose_name=_(u'Gender'), blank=True, null=True)

    countryoforigin = models.ForeignKey('Country', verbose_name=_(u'Country'), blank=True, null=True)
    primarydisease = models.ForeignKey('Disease', verbose_name=_(u'Disease'), blank=True, null=True)
    diseaseadditionalinfo = models.CharField(_(u'Disease additional info'), max_length=45, blank=True)
    othercelllinefromdonor = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), related_name='celllines_othercelllinefromdonor', blank=True, null=True)
    parentcellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), related_name='celllines_parentcellline', blank=True, null=True)
    providerdonorid = models.CharField(_(u'Provider donor id'), max_length=45, blank=True)
    cellabnormalkaryotype = models.CharField(_(u'Cell abnormal karyotype'), max_length=45, blank=True)
    donorabnormalkaryotype = models.CharField(_(u'Donor abnormal karyotype'), max_length=45, blank=True)
    otherclinicalinformation = models.CharField(_(u'Other clinical information'), max_length=100, blank=True)
    phenotype = models.ForeignKey('Phenotype', verbose_name=_(u'Phenotype'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Donor')
        verbose_name_plural = _(u'Donors')
        ordering = ['biosamplesid']

    def __unicode__(self):
        return u'%s' % (self.biosamplesid,)


class Ebisckeyword(models.Model):
    cellline = models.ForeignKey('Cellline', verbose_name=_(u'Cell line'), blank=True, null=True)
    document = models.ForeignKey('Document', verbose_name=_(u'Document'), blank=True, null=True)
    ebisckeyword = models.ForeignKey('Keyword', verbose_name=_(u'Keyword'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Ebisc keyword')
        verbose_name_plural = _(u'Ebisc keywords')
        ordering = ['cellline', 'document', 'ebisckeyword']

    def __unicode__(self):
        return u'%s - %s - %s' % (self.cellline, self.document, self.ebisckeyword)


class Enzymatically(models.Model):
    name = models.CharField(_(u'Enzymatically'), max_length=45, unique=True)

    class Meta:
        verbose_name = _(u'Enzymatically')
        verbose_name_plural = _(u'Enzymatically')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class EnzymeFree(models.Model):
    name = models.CharField(_(u'Enzyme free'), max_length=45, unique=True)

    class Meta:
        verbose_name = _(u'Enzyme free')
        verbose_name_plural = _(u'Enzyme free')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class Germlayer(models.Model):
    germlayer = models.CharField(_(u'Germ layer'), max_length=15, blank=True)

    class Meta:
        verbose_name = _(u'Germ layer')
        verbose_name_plural = _(u'Germ layers')
        ordering = ['germlayer']

    def __unicode__(self):
        return u'%s' % (self.germlayer,)


class Hla(models.Model):
    hla = models.CharField(_(u'HLA'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'HLA')
        verbose_name_plural = _(u'HLAs')
        ordering = ['hla']

    def __unicode__(self):
        return u'%s' % (self.hla,)


class KaryotypeMethod(models.Model):
    name = models.CharField(_(u'Karyotype method'), max_length=45, unique=True)

    class Meta:
        verbose_name = _(u'Karyotype method')
        verbose_name_plural = _(u'Karyotype methods')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class Keyword(models.Model):
    keyword = models.CharField(_(u'Keyword'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Keyword')
        verbose_name_plural = _(u'Keywords')
        ordering = ['keyword']

    def __unicode__(self):
        return u'%s' % (self.keyword,)


class Marker(models.Model):
    marker = models.CharField(_(u'Marker'), max_length=20, blank=True)

    class Meta:
        verbose_name = _(u'Marker')
        verbose_name_plural = _(u'Markers')
        ordering = ['marker']

    def __unicode__(self):
        return u'%s' % (self.marker,)


class Molecule(models.Model):
    moleculename = models.CharField(_(u'Molecule name'), max_length=45, blank=True)
    referencesource = models.CharField(_(u'Reference source'), max_length=45, blank=True)
    referencesourceid = models.CharField(_(u'Reference source id'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Molecule')
        verbose_name_plural = _(u'Molecules')
        ordering = ['moleculename']

    def __unicode__(self):
        return u'%s' % (self.moleculename,)


class Morphologymethod(models.Model):
    morphologymethod = models.CharField(_(u'Morphology method'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Morphology method')
        verbose_name_plural = _(u'Morphology methods')
        ordering = ['morphologymethod']

    def __unicode__(self):
        return u'%s' % (self.morphologymethod,)


class Organization(models.Model):
    organizationname = models.CharField(_(u'Organization name'), max_length=100, unique=True, null=True, blank=True)
    organizationshortname = models.CharField(_(u'Organization short name'), unique=True, max_length=6, null=True, blank=True)
    organizationcontact = models.ForeignKey('Contact', verbose_name=_(u'Contact'), blank=True, null=True)
    organizationtype = models.ForeignKey('Orgtype', verbose_name=_(u'Orgtype'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Organization')
        verbose_name_plural = _(u'Organizations')
        ordering = ['organizationname', 'organizationshortname']

    def __unicode__(self):
        return u' - '.join([x for x in self.organizationshortname, self.organizationname if x])


class Orgtype(models.Model):
    orgtype = models.CharField(_(u'Org type'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Organization type')
        verbose_name_plural = _(u'Organization types')
        ordering = ['orgtype']

    def __unicode__(self):
        return u'%s' % (self.orgtype,)


class PassageMethod(models.Model):

    name = models.CharField(_(u'Passage method'), max_length=45, unique=True)

    class Meta:
        verbose_name = _(u'Passage method')
        verbose_name_plural = _(u'Passage methods')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class Person(models.Model):
    organization = models.IntegerField(_(u'Organization'), blank=True, null=True)
    personlastname = models.CharField(_(u'Person last name'), max_length=20, blank=True)
    personfirstname = models.CharField(_(u'Person first name'), max_length=45, blank=True)
    personcontact = models.ForeignKey('Contact', verbose_name=_(u'Contact'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Person')
        verbose_name_plural = _(u'Persons')
        ordering = ['personlastname', 'personfirstname']

    def __unicode__(self):
        return u'%s %s' % (self.personlastname, self.personfirstname)


class Phenotype(models.Model):
    phenotype = models.CharField(_(u'Phenotype'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Phenotype')
        verbose_name_plural = _(u'Phenotypes')
        ordering = ['phenotype']

    def __unicode__(self):
        return u'%s' % (self.phenotype,)


class Phonecountrycode(models.Model):
    phonecountrycode = models.DecimalField(_(u'Phone country code'), max_digits=4, decimal_places=0, blank=True, null=True)

    class Meta:
        verbose_name = _(u'Phone country code')
        verbose_name_plural = _(u'Phone country codes')
        ordering = ['phonecountrycode']

    def __unicode__(self):
        return u'%s' % (self.phonecountrycode,)


class Postcode(models.Model):
    postcode = models.CharField(_(u'Postcode'), max_length=45, blank=True)
    district = models.CharField(_(u'District'), max_length=20)

    class Meta:
        verbose_name = _(u'Postcode')
        verbose_name_plural = _(u'Postcodes')
        ordering = ['postcode', 'district']

    def __unicode__(self):
        return u'%s %s' % (self.postcode, self.district)


class PrimaryCellDevelopmentalStage(models.Model):
    name = models.CharField(_(u'Primary cell developmental stage'), max_length=20, unique=True)

    class Meta:
        verbose_name = _(u'Primary cell developmental stage')
        verbose_name_plural = _(u'Primary cell developmental stages')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class ProteinSource(models.Model):
    name = models.CharField(_(u'Protein source'), max_length=45, unique=True)

    class Meta:
        verbose_name = _(u'Protein source')
        verbose_name_plural = _(u'Protein sources')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class Publisher(models.Model):
    publisher = models.CharField(_(u'Publisher'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Publisher')
        verbose_name_plural = _(u'Publishers')
        ordering = ['publisher']

    def __unicode__(self):
        return u'%s' % (self.publisher,)


class Reprogrammingmethod1(models.Model):
    reprogrammingmethod1 = models.CharField(_(u'Reprogramming method 1'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Reprogramming method 1')
        verbose_name_plural = _(u'Reprogramming methods 1')
        ordering = ['reprogrammingmethod1']

    def __unicode__(self):
        return u'%s' % (self.reprogrammingmethod1,)


class Reprogrammingmethod2(models.Model):
    reprogrammingmethod2 = models.CharField(_(u'Reprogramming method 2'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Reprogramming method 2')
        verbose_name_plural = _(u'Reprogramming methods 2')
        ordering = ['reprogrammingmethod2']

    def __unicode__(self):
        return u'%s' % (self.reprogrammingmethod2,)


class Reprogrammingmethod3(models.Model):
    reprogrammingmethod3 = models.CharField(_(u'Reprogramming method 3'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Reprogramming method 3')
        verbose_name_plural = _(u'Reprogramming methods 3')
        ordering = ['reprogrammingmethod3']

    def __unicode__(self):
        return u'%s' % (self.reprogrammingmethod3,)


class Strfplocus(models.Model):
    strfplocus = models.CharField(_(u'STR FP locus'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'STR FP locus')
        verbose_name_plural = _(u'STR FP loci')
        ordering = ['strfplocus']

    def __unicode__(self):
        return u'%s' % (self.strfplocus,)


class SurfaceCoating(models.Model):
    name = models.CharField(_(u'Surface coating'), max_length=45, unique=True)

    class Meta:
        verbose_name = _(u'Surface coating')
        verbose_name_plural = _(u'Surface coatings')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class Tissuesource(models.Model):
    tissuesource = models.CharField(_(u'Tissue source'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Tissue source')
        verbose_name_plural = _(u'Tissue sources')
        ordering = ['tissuesource']

    def __unicode__(self):
        return u'%s' % (self.tissuesource,)


class Unit(models.Model):
    name = models.CharField(_(u'Units'), max_length=20)

    class Meta:
        verbose_name = _(u'Units')
        verbose_name_plural = _(u'Units')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class Useraccount(models.Model):
    username = models.CharField(_(u'Username'), max_length=45, blank=True)
    useraccounttype = models.ForeignKey('Useraccounttype', verbose_name=_(u'User account type'), blank=True, null=True)
    person = models.ForeignKey('Person', verbose_name=_(u'Person'), blank=True, null=True)
    organization = models.ForeignKey('Organization', verbose_name=_(u'Organization'), blank=True, null=True)
    accesslevel = models.ForeignKey('Accesslevel', verbose_name=_(u'Access level'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'User account')
        verbose_name_plural = _(u'User accounts')
        ordering = ['username']

    def __unicode__(self):
        return u'%s' % (self.username,)


class Useraccounttype(models.Model):
    useraccounttype = models.CharField(_(u'User account type'), max_length=15)

    class Meta:
        verbose_name = _(u'User account type')
        verbose_name_plural = _(u'User account types')
        ordering = ['useraccounttype']

    def __unicode__(self):
        return u'%s' % (self.useraccounttype,)


class Vectorfreereprogramfactor(models.Model):
    vectorfreereprogramfactor = models.CharField(_(u'Vector free reprogram factor'), max_length=15, blank=True)
    referenceid = models.CharField(_(u'Referenceid'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Vector free reprogram factor')
        verbose_name_plural = _(u'Vector free reprogram factors')
        ordering = ['vectorfreereprogramfactor']

    def __unicode__(self):
        return u'%s' % (self.vectorfreereprogramfactor,)


# -----------------------------------------------------------------------------
# Cell line vector

class NonIntegratingVector(models.Model):
    name = models.CharField(_(u'Non-integrating vector'), max_length=20, unique=True)

    class Meta:
        verbose_name = _(u'Non-integrating vector')
        verbose_name_plural = _(u'Non-integrating vectors')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class IntegratingVector(models.Model):
    name = models.CharField(_(u'Integrating vector'), max_length=20, unique=True)

    class Meta:
        verbose_name = _(u'Integrating vector')
        verbose_name_plural = _(u'Integrating vectors')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class Virus(models.Model):
    name = models.CharField(_(u'Virus'), max_length=20, unique=True)

    class Meta:
        verbose_name = _(u'Virus')
        verbose_name_plural = _(u'Viruses')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class Transposon(models.Model):
    name = models.CharField(_(u'Transposon'), max_length=45, blank=True)

    class Meta:
        verbose_name = _(u'Transposon')
        verbose_name_plural = _(u'Transposons')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name,)


class CellLineNonIntegratingVector(models.Model):

    cell_line = models.OneToOneField(Cellline, verbose_name=_(u'Cell line'), related_name='non_integrating_vector')
    vector = models.ForeignKey(NonIntegratingVector, verbose_name=_(u'Non-integrating vector'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Cell line non integrating vector')
        verbose_name_plural = _(u'Cell line non integrating vectors')

    def __unicode__(self):
        return u'%s' % (self.vector,)


class CellLineIntegratingVector(models.Model):

    cell_line = models.OneToOneField(Cellline, verbose_name=_(u'Cell line'), related_name='integrating_vector')
    vector = models.ForeignKey(IntegratingVector, verbose_name=_(u'Integrating vector'), blank=True, null=True)

    virus = models.ForeignKey(Virus, verbose_name=_(u'Virus'), blank=True, null=True)
    transposon = models.ForeignKey(Transposon, verbose_name=_(u'Transposon'), blank=True, null=True)

    excisable = models.NullBooleanField(_(u'Excisable'), default=None, null=True, blank=True)

    class Meta:
        verbose_name = _(u'Cell line integrating vector')
        verbose_name_plural = _(u'Cell line integrating vectors')

    def __unicode__(self):
        return u'%s' % (self.vector,)

# -----------------------------------------------------------------------------
