from collections import namedtuple

from pkr.kard import Kard
from pkr.cli.parser import _create_kard
from .utils import pkrTestCase

class TestExt(pkrTestCase):
    pkr_folder = 'ext'
    ArgsStruct = namedtuple('ArgsStruct', 'name env features driver extra meta')

    def test_kard_features_order_is_deterministic(self):
        with open(str(self.env_test.path / 'meta1.yml'), 'r') as f:
            args = self.ArgsStruct(
                name='test',
                env='test',
                features='a,b',
                driver='compose',
                extra={},
                meta=f,
            )

            res = []
            for i in range(3):
                kard = _create_kard(args)
                res.append((kard.meta['features'], kard.extensions.extensions))
                self.assertEqual(repr(res[-1]), repr(res[0]))
                f.seek(0)
            self.assertEqual(res[0][0], ['a', 'b', 'ext_mock', 'auto-volume'])

    def test_ext_loaded_from_pkr_path(self):
        f = open(str(self.env_test.path / 'meta1.yml'), 'r')
        args = self.ArgsStruct(
            name='test',
            env='test',
            features='a,b',
            driver='compose',
            extra={},
            meta=f,
        )
        kard = _create_kard(args)
        self.assertIn('ext_mock', kard.extensions.extensions)
        self.assertIn({'test': 'Ok'}, kard.extensions.get_context_template_data())

    def test_ext_loaded_from_entrypoints_group_pkr_extensions(self):
        f = open(str(self.env_test.path / 'meta1.yml'), 'r')
        args = self.ArgsStruct(
            name='test',
            env='test',
            features='a,b',
            driver='compose',
            extra={},
            meta=f,
        )
        kard = _create_kard(args)
        self.assertIn('auto-volume', kard.extensions.extensions)
        self.assertIn('use_volume', kard.extensions.get_context_template_data()[1])