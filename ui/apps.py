from django.apps import AppConfig


class UiConfig(AppConfig):
    name = "ui"

    def ready(self) -> None:
        import ui.signals

        return super().ready()
