import csv

import logging
logger = logging.getLogger('management.commands')

from ebisc.celllines.models import Cellline, CelllineBatch, CelllineAliquot


'''Batch and vial biosamples IDs importer'''


# -----------------------------------------------------------------------------
#  Run

def run(filename):

    with open(filename, 'rb') as csvfile:

        reader = csv.reader(csvfile, delimiter='\t')

        next(reader, None)

        for row in reader:

            (vial_biosamples_id, _, _, cellline_biosamples_id, _, _, _, _, batch_biosamples_id) = row

            try:
                cell_line = Cellline.objects.get(biosamplesid=cellline_biosamples_id)
                batch = create_batch(cell_line, batch_biosamples_id)
                create_aliquot(batch, vial_biosamples_id)

            except Cellline.DoesNotExist:
                pass
                # logger.warn('Cell line with biosamples ID %s does not exists' % cellline_biosamples_id)


# -----------------------------------------------------------------------------
#  Utils

def create_batch(cell_line, batch_biosamples_id):

    batch, created = CelllineBatch.objects.get_or_create(
        cell_line=cell_line,
        batch_id=batch_biosamples_id,  # temporarily use batch_biosamples_id
        biosamplesid=batch_biosamples_id,
    )

    if created:
        logger.info('Created batch {} for cell line {}'.format(batch, cell_line))

    return batch


def create_aliquot(batch, aliquot_biosamples_id):

    aliquot, created = CelllineAliquot.objects.get_or_create(
        batch=batch,
        biosamplesid=aliquot_biosamples_id,
    )

    if created:
        logger.info('Created aliquot {} for cell line {} and batch {}'.format(aliquot, batch.cell_line, batch))

    return aliquot

# -----------------------------------------------------------------------------
