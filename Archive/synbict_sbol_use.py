import os, sbol2, argparse, logging
from sequences_to_features import FeatureLibrary, load_sbol, FeatureCurator, FeaturePruner, FeatureAnnotater, load_target_file, main

# pull sequences for every igem compdef!!!!!!

cwd = os.getcwd()

input_file_name = "igem_library.xml"

library_list = os.listdir(os.path.join(cwd, 'libraries'))
library_list = [os.path.join(cwd, 'libraries', x) for x in library_list]
# library_list = ' '.join(library_list)


logger_file_name = os.path.join(cwd, 'sbol_synbict_log.txt')

# print(library_list)

args = ['-n', 'http://mynamespace.org', '-t', os.path.join(cwd, input_file_name), '-s', 'annotated', '-f', library_list,
             '-l', logger_file_name, '-m', '10', '-d', '-ni']

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # Common arguments
    parser.add_argument('-n', '--namespace')
    parser.add_argument('-t', '--target_files', nargs='*', default=[])
    parser.add_argument('-o', '--output_files', nargs='*', default=[])
    parser.add_argument('-s', '--output_suffix', nargs='?', default='')
    parser.add_argument('-p', '--in_place', action='store_true')
    parser.add_argument('-m', '--min_target_length', nargs='?', default=2000)
    parser.add_argument('-mo', '--minimal_output', action='store_true')
    parser.add_argument('-ni', '--non_interactive', action='store_true')
    parser.add_argument('-l', '--log_file', nargs='?', default='')
    parser.add_argument('-v', '--validate', action='store_true')

    # Sequence annotation arguments
    parser.add_argument('-f', '--feature_files', nargs='*', default=[])
    parser.add_argument('-M', '--min_feature_length', nargs='?', default=40)
    
    parser.add_argument('-na', '--no_annotation', action='store_true')
    parser.add_argument('-e', '--extend_features', action='store_true')
    parser.add_argument('-xs', '--extension_suffix', nargs='?', default='')
    parser.add_argument('-x', '--extension_threshold', nargs='?', default=0.05)

    # Annotation pruning arguments
    parser.add_argument('-c', '--cover_offset', nargs='?', default=14)
    parser.add_argument('-r', '--deletion_roles', nargs='*', default=[])
    parser.add_argument('-d', '--delete_flat', action='store_true')
    parser.add_argument('-np', '--no_pruning', action='store_true')
    parser.add_argument('-a', '--auto_swap', action='store_true')
    
    # parser.add_argument('-s', '--sbh_URL', nargs='?', default=None)
    # parser.add_argument('-u', '--username', nargs='?', default=None)
    # parser.add_argument('-p', '--password', nargs='?', default=None)
    # parser.add_argument('-F', '--feature_URLs', nargs='*', default=[])
    # parser.add_argument('-T', '--target_URLs', nargs='*', default=[])
    # parser.add_argument('-o', '--sbh_output_file', nargs='?', default=None)
    
    args = parser.parse_args(args)

    logger = logging.getLogger('synbict')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s ; %(levelname)s ; %(message)s')

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    if len(args.log_file) > 0:
        file_handler = logging.FileHandler(args.log_file, "w")
        file_handler.setLevel(logging.DEBUG)

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    sbol2.setHomespace(args.namespace)
    sbol2.Config.setOption('validate', args.validate)
    sbol2.Config.setOption('sbol_typed_uris', False)

    target_files = []
    for target_file in args.target_files:
        if os.path.isdir(target_file):
            target_files.extend([os.path.join(target_file, tf) for tf in os.listdir(target_file) if
                                 os.path.isfile(os.path.join(target_file, tf)) and (tf.endswith('.xml') or
                                                                                    tf.endswith('.sbol') or
                                                                                    tf.endswith('.gb') or
                                                                                    tf.endswith('.genbank') or
                                                                                    tf.endswith('.fasta') or
                                                                                    tf.endswith('.faa') or
                                                                                    tf.endswith('.fa') or
                                                                                    tf.endswith('.fas') or
                                                                                    tf.endswith('.fsa'))])
        else:
            target_files.append(target_file)

    output_files = []
    for i in range(0, len(target_files)):
        if len(args.output_files) == 1 and os.path.isdir(args.output_files[0]):
            (target_file_path, target_filename) = os.path.split(target_files[i])
            (target_file_base, target_file_extension) = os.path.splitext(target_filename)

            if len(args.output_suffix) > 0:
                output_files.append(os.path.join(args.output_files[0], '_'.join([target_file_base, args.output_suffix + '.xml'])))
            else:
                output_files.append(os.path.join(args.output_files[0], target_file_base + '.xml'))
        elif i < len(args.output_files):
            output_files.append(args.output_files[i])
        else:
            (target_file_base, target_file_extension) = os.path.splitext(target_files[i])

            if len(args.output_suffix) > 0:
                output_files.append('_'.join([target_file_base, args.output_suffix + '.xml']))
            else:
                output_files.append(target_file_base + '.xml')

    

    if isinstance(args.feature_files[0], list):
        args.feature_files = args.feature_files[0]
    
    feature_docs = []
    for feature_file in args.feature_files:
        feature_docs.append(load_sbol(feature_file))

    feature_library = FeatureLibrary(feature_docs)

    if args.extend_features or not args.no_annotation:
        feature_annotater = FeatureAnnotater(feature_library, int(args.min_feature_length))

    if args.extend_features:
        target_docs = []
        for target_file in target_files:
            target_docs.append(load_target_file(target_file))
        for i in range(len(target_files) - 1, -1, -1):
            if not target_docs[i]:
                del target_docs[i]
                del target_files[i]
                del output_files[i]

        target_library = FeatureLibrary(target_docs)

        if args.minimal_output:
            output_docs = [sbol2.Document() for i in range(0, len(target_library.docs))]
        else:
            output_docs = []

        output_library = FeatureLibrary(output_docs, False)

        feature_curator = FeatureCurator(target_library, output_library)
        feature_curator.extend_features(feature_annotater,
                                        int(args.min_target_length),
                                        float(args.extension_threshold))

        for extended_doc in feature_annotater.get_updated_documents():
            if len(args.extension_suffix) > 0:
                (extended_file_base, extended_file_extension) = os.path.splitext(extended_doc.name)

                extended_file = '_'.join([extended_file_base, args.extension_suffix]) + '.xml'
            else:
                extended_file = extended_doc.name

            logger.info('Writing %s', extended_file)

            extended_doc.write(extended_file)

        if not args.no_annotation:
            (annotated_features, annotating_features) = feature_curator.annotate_features(feature_annotater,
                                                                                          int(args.min_target_length),
                                                                                          args.in_place)

            if args.minimal_output:
                for i in range(0, len(output_library.docs)):
                    if len(output_library.docs[i].componentDefinitions) == 0:
                        logger.warning('Failed to annotate %s, possibly no constructs found with minimum length %s',
                                        target_files[i], args.min_target_length)
            else:
                for i in target_library.get_non_updated_indices():
                    logger.warning('Failed to annotate %s, possibly no constructs found with minimum length %s',
                                    target_files[i], args.min_target_length)
        else:
            annotated_features = []
            annotating_features = []

        if not args.no_pruning:
            feature_pruner = FeaturePruner(feature_library, set(args.deletion_roles))
            feature_curator.prune_features(feature_pruner,
                                           int(args.cover_offset),
                                           int(args.min_target_length),
                                           annotated_features,
                                           annotating_features,
                                           args.delete_flat,
                                           args.auto_swap,
                                           not args.non_interactive)

        if not args.no_annotation or not args.no_pruning:
            if len(output_docs) > 0:
                for i in range(0, len(output_docs)):
                    if sbol2.Config.getOption('validate') == True:
                        logger.info('Validating and writing %s', output_files[i])
                    else:
                        logger.info('Writing %s', output_files[i])

                    output_docs[i].write(output_files[i])
            else:
                for i in range(0, len(target_docs)):
                    if sbol2.Config.getOption('validate') == True:
                        logger.info('Validating and writing %s', output_files[i])
                    else:
                        logger.info('Writing %s', output_files[i])

                    target_docs[i].write(output_files[i])
    else:
        for i in range(0, len(target_files)):
            target_doc = load_target_file(target_files[i])

            if target_doc:
                target_library = FeatureLibrary([target_doc])

                if args.minimal_output:
                    output_docs = [sbol2.Document()]
                else:
                    output_docs = []

                output_library = FeatureLibrary(output_docs, False)

                feature_curator = FeatureCurator(target_library, output_library)

                if not args.no_annotation:
                    (annotated_features, annotating_features) = feature_curator.annotate_features(feature_annotater,
                                                                                                  int(args.min_target_length),
                                                                                                  args.in_place)

                    if args.minimal_output:
                        if len(output_library.docs[i].componentDefinitions) == 0:
                            logger.warning('Failed to annotate %s, possibly no constructs found with minimum length %s',
                                            target_files[i], args.min_target_length)
                    elif len(target_library.get_non_updated_indices()) > 0:
                        logger.warning('Failed to annotate %s, possibly no constructs found with minimum length %s',
                                        target_files[i], args.min_target_length)


                if not args.no_pruning:
                    feature_pruner = FeaturePruner(feature_library, set(args.deletion_roles))
                    feature_curator.prune_features(feature_pruner,
                                                   int(args.cover_offset),
                                                   int(args.min_target_length),
                                                   annotated_features,
                                                   annotating_features,
                                                   args.delete_flat,
                                                   args.auto_swap,
                                                   not args.non_interactive)

                if not args.no_annotation or not args.no_pruning:
                    if len(output_docs) == 1:
                        if sbol2.Config.getOption('validate') == True:
                            logger.info('Validating and writing %s', output_files[i])
                        else:
                            logger.info('Writing %s', output_files[i])

                        output_docs[0].write(output_files[i])
                    else:
                        if sbol2.Config.getOption('validate') == True:
                            logger.info('Validating and writing %s', output_files[i])
                        else:
                            logger.info('Writing %s', output_files[i])

                        target_doc.write(output_files[i])

    logger.info('Finished curating')

main(args)