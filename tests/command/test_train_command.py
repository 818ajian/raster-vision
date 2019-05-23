import unittest

import rastervision as rv
from rastervision.rv_config import RVConfig

import tests.mock as mk


class TrainCommand(mk.MockMixin, unittest.TestCase):
    def test_missing_config_task(self):
        with self.assertRaises(rv.ConfigError):
            rv.CommandConfig.builder(rv.TRAIN) \
                            .with_backend('') \
                            .build()

    def test_missing_config_backend(self):
        with self.assertRaises(rv.ConfigError):
            rv.CommandConfig.builder(rv.TRAIN) \
                            .with_task('') \
                            .build()

    def test_no_config_error(self):
        task = rv.task.ChipClassificationConfig({})
        backend = rv.backend.KerasClassificationConfig('')
        try:
            with RVConfig.get_tmp_dir() as tmp_dir:
                rv.CommandConfig.builder(rv.TRAIN) \
                                .with_task(task) \
                                .with_root_uri(tmp_dir) \
                                .with_backend(backend) \
                                .build()
        except rv.ConfigError:
            self.fail('rv.ConfigError raised unexpectedly')

    def test_command_run_with_mocks(self):
        task_config = rv.TaskConfig.builder(mk.MOCK_TASK).build()
        backend_config = rv.BackendConfig.builder(mk.MOCK_BACKEND).build()
        backend = backend_config.create_backend(task_config)

        cmd_conf = rv.CommandConfig.builder(rv.TRAIN) \
                                   .with_task(task_config) \
                                   .with_backend(backend_config) \
                                   .with_root_uri('.') \
                                   .build()

        cmd_conf = rv.command.CommandConfig.from_proto(cmd_conf.to_proto())

        cmd_conf.backend.mock.create_backend.return_value = backend

        cmd = cmd_conf.create_command()

        cmd.run()

        self.assertTrue(backend.mock.train.called)


if __name__ == '__main__':
    unittest.main()
