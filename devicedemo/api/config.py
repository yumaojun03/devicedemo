from devicedemo.api import hooks


app = {
    'root': 'devicedemo.api.controllers.root.RootController',
    'modules': ['devicedemo.api'],
    'hooks': [
            hooks.DBHook(),
        ],
    'debug': False,
}
