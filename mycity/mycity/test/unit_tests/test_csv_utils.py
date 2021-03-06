import csv
import collections
import unittest.mock as mock

import mycity.test.test_constants as test_constants
import mycity.test.unit_tests.base as base
import mycity.utilities.csv_utils as csv_utils



class CSVUtilitiesTestCase(base.BaseTestCase):

    def test_create_record_model_with_arbitrary_fields(self):
        Record = collections.namedtuple('TestRecord', ['field_1', 'field_2'])
        attributes = ['field_1', 'field_2']
        model = csv_utils.create_record_model('TestRecord', attributes)
        to_test = model(4, 5)
        self.assertEqual(to_test.field_1, 4)
        self.assertEqual(to_test.field_2, 5)

    def test_create_record_model_with_csv_header(self):
        test_file = test_constants.PARKING_LOTS_TEST_CSV
        attributes = None
        with open(test_file, encoding='utf-8-sig') as f:
            csv_file = csv.reader(f, delimiter = ',')
            attributes = next(csv_file)           
            model = csv_utils.create_record_model('TestRecord', attributes)
        for attribute in attributes:
            self.assertTrue(hasattr(model, attribute))

    def test_csv_to_namedtuples(self):
        test_file = test_constants.PARKING_LOTS_TEST_CSV
        fields = ['X','Y','FID','OBJECTID','Spaces','Fee','Comments','Phone',
                  'Name','Address', 'Neighborho','Maxspaces','Hours','GlobalID',
                  'CreationDate','Creator', 'EditDate','Editor']
        Record = collections.namedtuple('Record', fields)
        with open(test_file, encoding='utf-8-sig') as csv_file:
            reader = csv.reader(csv_file, delimiter = ',')
            next(reader)                         # remove header
            to_test = csv_utils.csv_to_namedtuples(Record, reader)
        for item in to_test:
            self.assertIsInstance(item, Record)

    def test_csv_to_namedtuples_address_field_not_null(self):
        test_file = test_constants.PARKING_LOTS_TEST_CSV
        fields = ['X','Y','FID','OBJECTID','Spaces','Fee','Comments','Phone',
                  'Name','Address', 'Neighborho','Maxspaces','Hours','GlobalID',
                  'CreationDate','Creator', 'EditDate','Editor']
        Record = collections.namedtuple('Record', fields)
        with open(test_file, encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            next(csv_reader)    # remove header
            records = csv_utils.csv_to_namedtuples(Record, csv_reader)
        for record_to_test in records:
            self.assertIsNotNone(record_to_test.Address)

    def test_add_city_and_state_to_records(self):
        records = []        
        records.append({'test_field':'wes', 'Address': '1000 Dorchester Ave'})
        records.append({'test_field':'drew', 'Address':'123 Fake St'})
        to_test = csv_utils.add_city_and_state_to_records(records, 'Address', 'Boston', 'MA')
        for record in to_test:
            self.assertIn("Boston, MA", record['Address'])

    def test_map_attribute_to_record(self):
        Record = collections.namedtuple('Record', ['test_field', 'Address'])
        records = []
        records.append(Record('wes', '1000 Dorchester Ave'))
        records.append(Record('drew', '123 Fake St'))
        to_test = csv_utils.map_attribute_to_records('Address', records)
        self.assertEqual(records[0], to_test['1000 Dorchester Ave'])


