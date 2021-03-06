
#!/usr/bin/env python
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown


class DDApp(App):
    def build(self):
        bm = GridLayout(cols=2)
        bm.add_widget(Label(text='choose'))
        dropdown = DropDown()

        for index in range(10):
            btn = Button(text='Value %d' % index, size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        mainbutton = Button(text='Hello', size_hint=(None, None))
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(
            on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        bm.add_widget(mainbutton)
        return bm

if __name__ == '__main__':
    DDApp().run()