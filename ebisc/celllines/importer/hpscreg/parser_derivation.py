import logging
logger = logging.getLogger('management.commands')

from django.db import IntegrityError

from .utils import format_integrity_error

from .parser import inject_valuef, value_of_file, term_list_value_of_json, parse_molecule

from ebisc.celllines.models import \
    Virus,  \
    Transposon,  \
    CellType,  \
    CelllineDerivation, \
    NonIntegratingVector,  \
    IntegratingVector,  \
    CelllineNonIntegratingVector,  \
    CelllineIntegratingVector,  \
    CelllineVectorFreeReprogrammingFactors,  \
    VectorFreeReprogrammingFactor


# -----------------------------------------------------------------------------

@inject_valuef
def parse_reprogramming_vector(valuef, source, cell_line):

    if valuef('vector_type') == 'Integrating':
        try:
            v = CelllineNonIntegratingVector.objects.get(cell_line=cell_line)
            v.delete()
            return True
        except CelllineNonIntegratingVector.DoesNotExist:
            pass
        return parse_integrating_vector(source, cell_line)

    elif valuef('vector_type') == 'Non-integrating':
        try:
            v = CelllineIntegratingVector.objects.get(cell_line=cell_line)
            v.delete()
            return True
        except CelllineIntegratingVector.DoesNotExist:
            pass
        return parse_non_integrating_vector(source, cell_line)

    else:
        return False


@inject_valuef
def parse_integrating_vector(valuef, source, cell_line):

    if valuef('integrating_vector') == 'Other':
        if valuef('integrating_vector_other') is not None:
            vector_name = valuef('integrating_vector_other')
        else:
            vector_name = u'Other'
    else:
        vector_name = valuef('integrating_vector')

    if vector_name is None:
        logger.warn('Missing name for integrating reprogramming vector')
        return False

    vector, vector_created = IntegratingVector.objects.get_or_create(name=vector_name)

    if vector_created:
        logger.info('Added integrating vector: %s' % vector)

    cell_line_integrating_vector, cell_line_integrating_vector_created = CelllineIntegratingVector.objects.get_or_create(cell_line=cell_line)

    cell_line_integrating_vector.vector = vector
    cell_line_integrating_vector.virus = term_list_value_of_json(source, 'integrating_vector_virus_type', Virus)
    cell_line_integrating_vector.transposon = term_list_value_of_json(source, 'integrating_vector_transposon_type', Transposon)
    cell_line_integrating_vector.excisable = valuef('excisable_vector_flag', 'bool')
    cell_line_integrating_vector.absence_reprogramming_vectors = valuef('reprogramming_vectors_absence_flag', 'bool')

    if valuef('reprogramming_vector_integrating_silenced_flag'):
        cell_line_integrating_vector.silenced = valuef('reprogramming_vector_integrating_silenced_flag', 'extended_bool')
    cell_line_integrating_vector.methods = valuef('reprogramming_vector_integrating_method')
    cell_line_integrating_vector.silenced_notes = valuef('reprogramming_vector_integrating_silencing_notes')

    cell_line_integrating_vector.save()

    # Parse expressed, silenced detection file
    if cell_line_integrating_vector.expressed_silenced_file_enc:
        expressed_silenced_file_current_enc = cell_line_integrating_vector.expressed_silenced_file_enc
    else:
        expressed_silenced_file_current_enc = None

    # Save or update a file if it exists
    if valuef('reprogramming_vector_integrating_silencing_file'):
        cell_line_integrating_vector.expressed_silenced_file_enc = value_of_file(valuef('reprogramming_vector_integrating_silencing_file_enc'), valuef('reprogramming_vector_integrating_silencing_file'), cell_line_integrating_vector.expressed_silenced_file, expressed_silenced_file_current_enc)

        cell_line_integrating_vector.save()

    # Delete old file if it is no longer in the export
    elif cell_line_integrating_vector.expressed_silenced_file_enc:
        logger.info('Deleting obsolete reprogramming silencing file %s' % cell_line_integrating_vector.expressed_silenced_file)
        cell_line_integrating_vector.expressed_silenced_file.delete()
        cell_line_integrating_vector.expressed_silenced_file_enc = None

    # Parse vector map file
    if cell_line_integrating_vector.vector_map_file_enc:
        vector_map_file_current_enc = cell_line_integrating_vector.vector_map_file_enc
    else:
        vector_map_file_current_enc = None

    # Save or update a file if it exists
    if valuef('vector_map_file_enc'):
        cell_line_integrating_vector.vector_map_file_enc = value_of_file(valuef('vector_map_file_enc'), valuef('vector_map_file'), cell_line_integrating_vector.vector_map_file, vector_map_file_current_enc)

        cell_line_integrating_vector.save()

    # Delete old file if it is no longer in the export
    elif cell_line_integrating_vector.vector_map_file_enc:
        logger.info('Deleting obsolete reprogramming detection file %s' % cell_line_integrating_vector.vector_map_file)
        cell_line_integrating_vector.vector_map_file.delete()
        cell_line_integrating_vector.vector_map_file_enc = None

    dirty = [cell_line_integrating_vector.is_dirty(check_relationship=True)]

    for gene in [parse_molecule(g) for g in source.get('integrating_vector_gene_list', [])]:
        cell_line_integrating_vector.genes.add(gene)

    if True in dirty:
        if cell_line_integrating_vector_created:
            logger.info('Added integrating vector: %s to cell line %s' % (vector, cell_line))
        else:
            logger.info('Updated integrating vector: %s to cell line %s' % (vector, cell_line))

        cell_line_integrating_vector.save()

        return True

    return False


@inject_valuef
def parse_non_integrating_vector(valuef, source, cell_line):

    if valuef('non_integrating_vector') == 'Other':
        if valuef('non_integrating_vector_other') is not None:
            vector_name = valuef('non_integrating_vector_other')
        else:
            vector_name = u'Other'
    else:
        vector_name = valuef('non_integrating_vector')

    if vector_name is None:
        logger.warn('Missing name for non integrating reprogramming vector')
        return False

    vector, vector_created = NonIntegratingVector.objects.get_or_create(name=vector_name)

    if vector_created:
        logger.info('Added non-integrating vector: %s' % vector)

    cell_line_non_integrating_vector, cell_line_non_integrating_vector_created = CelllineNonIntegratingVector.objects.get_or_create(cell_line=cell_line)

    cell_line_non_integrating_vector.vector = vector

    dirty = [cell_line_non_integrating_vector.is_dirty(check_relationship=True)]

    for gene in [parse_molecule(g) for g in source.get('non_integrating_vector_gene_list', [])]:
        cell_line_non_integrating_vector.genes.add(gene)

    if valuef('reprogramming_vector_non_integrating_detectable_flag'):
        cell_line_non_integrating_vector.detectable = valuef('reprogramming_vector_non_integrating_detectable_flag', 'extended_bool')
    cell_line_non_integrating_vector.methods = valuef('reprogramming_vector_non_integrating_method')
    cell_line_non_integrating_vector.detectable_notes = valuef('reprogramming_vector_non_integrating_detection_notes')

    # Parse expressed, silenced detection file
    if cell_line_non_integrating_vector.expressed_silenced_file_enc:
        expressed_silenced_file_current_enc = cell_line_non_integrating_vector.expressed_silenced_file_enc
    else:
        expressed_silenced_file_current_enc = None

    # Save or update a file if it exists
    if valuef('reprogramming_vector_non_integrating_detection_file_enc'):
        cell_line_non_integrating_vector.expressed_silenced_file_enc = value_of_file(valuef('reprogramming_vector_non_integrating_detection_file_enc'), valuef('reprogramming_vector_non_integrating_detection_file'), cell_line_non_integrating_vector.expressed_silenced_file, expressed_silenced_file_current_enc)

        cell_line_non_integrating_vector.save()

    # Delete old file if it is no longer in the export
    elif cell_line_non_integrating_vector.expressed_silenced_file_enc:
        logger.info('Deleting obsolete reprogramming detection file %s' % cell_line_non_integrating_vector.expressed_silenced_file)
        cell_line_non_integrating_vector.expressed_silenced_file.delete()
        cell_line_non_integrating_vector.expressed_silenced_file_enc = None

    # Parse vector map file
    if cell_line_non_integrating_vector.vector_map_file_enc:
        vector_map_file_current_enc = cell_line_non_integrating_vector.vector_map_file_enc
    else:
        vector_map_file_current_enc = None

    # Save or update a file if it exists
    if valuef('vector_map_file_enc'):
        cell_line_non_integrating_vector.vector_map_file_enc = value_of_file(valuef('vector_map_file_enc'), valuef('vector_map_file'), cell_line_non_integrating_vector.vector_map_file, vector_map_file_current_enc)

        cell_line_non_integrating_vector.save()

    # Delete old file if it is no longer in the export
    elif cell_line_non_integrating_vector.vector_map_file_enc:
        logger.info('Deleting obsolete reprogramming detection file %s' % cell_line_non_integrating_vector.vector_map_file)
        cell_line_non_integrating_vector.vector_map_file.delete()
        cell_line_non_integrating_vector.vector_map_file_enc = None

    if True in dirty:
        if cell_line_non_integrating_vector_created:
            logger.info('Added non-integrationg vector %s to cell line %s' % (vector, cell_line))
        else:
            logger.info('Updated non-integrationg vector %s to cell line %s' % (vector, cell_line))

        cell_line_non_integrating_vector.save()

        return True

    return False


def parse_vector_free_reprogramming_factor(factor):

    factor, created = VectorFreeReprogrammingFactor.objects.get_or_create(name=factor)

    if created:
        logger.info('Created new vector free reprogramming factor: %s' % factor)

    return factor


@inject_valuef
def parse_vector_free_reprogramming_factors(valuef, source, cell_line):

    if valuef('vector_free_types') is not None and valuef('vector_free_types'):
        cell_line_vector_free_reprogramming_factors, cell_line_vector_free_reprogramming_factors_created = CelllineVectorFreeReprogrammingFactors.objects.get_or_create(cell_line=cell_line)

        dirty = [cell_line_vector_free_reprogramming_factors.is_dirty(check_relationship=True)]

        for factor in [parse_vector_free_reprogramming_factor(f) for f in source.get('vector_free_types', [])]:
            cell_line_vector_free_reprogramming_factors.factors.add(factor)

        if True in dirty:
            try:
                cell_line_vector_free_reprogramming_factors.save()

                if cell_line_vector_free_reprogramming_factors_created:
                    logger.info('Added cell line vector free reprogramming factors: %s' % cell_line_vector_free_reprogramming_factors)
                else:
                    logger.info('Updated cell line vector free reprogramming factors: %s' % cell_line_vector_free_reprogramming_factors)

                return True

            except IntegrityError, e:
                logger.warn(format_integrity_error(e))
                return None

        return False


@inject_valuef
def parse_cell_type(valuef, source):

    value = valuef('primary_celltype_name')

    if value is None:
        return

    try:
        cell_type, created = CellType.objects.update_or_create(
            name=value,
            defaults={
                'purl': valuef('primary_celltype_ont_id'),
            }
        )
    except IntegrityError, e:
        logger.warn(format_integrity_error(e))
        return None

    if created:
        logger.info('Found new cell type: %s' % cell_type)

    return cell_type


@inject_valuef
def parse_derivation(valuef, source, cell_line):

    cell_line_derivation, cell_line_derivation_created = CelllineDerivation.objects.get_or_create(cell_line=cell_line)

    cell_line_derivation.primary_cell_type = parse_cell_type(source)
    cell_line_derivation.primary_cell_type_not_normalised = valuef('primary_celltype_name_freetext')
    cell_line_derivation.primary_cellline = valuef('primary_cell_line_name')
    cell_line_derivation.primary_cellline_vendor = valuef('primary_cell_line_vendor')
    cell_line_derivation.primary_cell_developmental_stage = valuef('dev_stage_primary_cell') if valuef('dev_stage_primary_cell') and valuef('dev_stage_primary_cell') != '0' else ''
    cell_line_derivation.tissue_procurement_location = valuef('location_primary_tissue_procurement')
    cell_line_derivation.tissue_collection_date = valuef('collection_date')
    cell_line_derivation.reprogramming_passage_number = valuef('passage_number_reprogrammed')

    cell_line_derivation.selection_criteria_for_clones = valuef('selection_of_clones')
    cell_line_derivation.xeno_free_conditions = valuef('derivation_xeno_graft_free_flag', 'bool')
    cell_line_derivation.derived_under_gmp = valuef('derivation_gmp_ips_flag', 'bool')
    cell_line_derivation.available_as_clinical_grade = valuef('available_clinical_grade_ips_flag', 'bool')

    if cell_line_derivation_created or cell_line_derivation.is_dirty(check_relationship=True):
        try:
            cell_line_derivation.save()

            if cell_line_derivation_created:
                logger.info('Added cell line derivation: %s' % cell_line_derivation)
            else:
                logger.info('Updated cell line derivation: %s' % cell_line_derivation)

            return True

        except IntegrityError, e:
            logger.warn(format_integrity_error(e))
            return None

    return False
