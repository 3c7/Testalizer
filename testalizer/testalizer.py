import click
import io
import os
import sys
import logging
import json
import re

from glob import glob


@click.command()
@click.argument('path')
def entrypoint(path):
    """Testalizer v. 0.1.0

    Testalizer can be used for testing cortex analyzers."""
    test(path)


def test(path: str):
    """
    Tests an analyzer.

    :param path: Path to one specific cortex analyzer
    :type path: str
    :return:
    """
    # Creates logging object
    logger = logging.getLogger('testalizer')
    logger.setLevel(logging.DEBUG)
    logging_fh = logging.FileHandler('testalizer.log')
    logging_fh.setLevel(logging.DEBUG)
    logging_sh = logging.StreamHandler()
    logging_sh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging_fh.setFormatter(formatter)
    logging_sh.setFormatter(formatter)
    logger.addHandler(logging_fh)
    logger.addHandler(logging_sh)

    # Using absolute path
    path = os.path.abspath(path)

    # Some path checks
    logger.debug('Start inspecting {}.'.format(path))
    if not os.path.exists(path):
        logger.error('Path does not exist.')
        exit(-1)

    if not os.path.isfile(path):
        # Grab the definition file
        definition_file = glob(path + '/*.json')
        logger.debug('Found files: {}'.format(definition_file))
        if len(definition_file) > 1:
            logger.warning('Multiple json files detected, using first in list: {}.'.format(definition_file[0]))
        definition_file = definition_file[0]
    else:
        definition_file = path
        path = os.path.dirname(path)
        if definition_file[-5:] != '.json':
            logger.error('{} ends with {} not .json'.format(definition_file, definition_file[-5:]))
            exit(-1)


    logger.debug('Opening definition file {}.'.format(definition_file))
    with io.open(definition_file, 'r') as fh:
        analyzer_definition = json.loads(fh.read())

    # Print infos and check for the important keys
    logger.info('ANALYZER INFORMATION')
    logger.info('====================')
    try:
        logger.info('Name: {}'.format(analyzer_definition['name']))
        logger.info('Author: {}'.format(analyzer_definition['author']))
        logger.info('Description: {}'.format(analyzer_definition['description']))
        logger.info('License: {}'.format(analyzer_definition['license']))
        logger.info('URL: {}'.format(analyzer_definition['url']))
        logger.info('Data types: {}'.format(analyzer_definition['dataTypeList']))
        logger.info('Command: {}'.format(analyzer_definition['command']))
    except KeyError as ke:
        logger.error('Required key in analyzer definition missing: {}'.format(ke.args))
        exit(-1)

    logger.info('')
    logger.info('ANALYZER CONFIGURATION')
    logger.info('======================')
    analyzer_config = analyzer_definition.get('config', {})
    if len(analyzer_config) == 0:
        logger.info('None.')
    for key, value in analyzer_config.items():
        logger.info('{}: {}'.format(key, value))

    # Get all necessary parameters
    logger.info('')
    logger.info('ANALYZER PARAMETERS')
    logger.info('===================')
    analyzer_file = analyzer_definition['command'].split('/')[1]
    logger.debug('Assuming analyzer file is {}.'.format(analyzer_file))
    with io.open(path + '/' + analyzer_file, 'r') as fh:
        analyzer_file_content = fh.read()

    parameters = re.findall(r'config\.[a-zA-Z]*', analyzer_file_content)
    logger.debug('Parameter regex search returned {}.'.format(parameters))
    if len(parameters) > 0:
        for p in parameters:
            logger.info(p[7:])
