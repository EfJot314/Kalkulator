from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.first = True
        self.last = True
        self.counted = False
        self.was = False

        tab = [
            ['1', '2', '3', '*'],
            ['4', '5', '6', '/'],
            ['7', '8', '9', '+'],
            ['0', 'AC', '^', '-'],
            ['=']
        ]

        self.actions = ['+', '-', '*', '/', '^', '=']

        self.equation = TextInput(
            multiline=False, readonly=True, halign='left'
        )
        layout.add_widget(self.equation)

        for row in tab:
            n_lay = BoxLayout()
            for num in row:
                button = Button(
                    text = num,
                    pos_hint = {'center_x': 0.5, 'center_y': 0.5}
                )
                button.bind(on_press = self.when_pressed)
                n_lay.add_widget(button)
            layout.add_widget(n_lay)

        return layout

    def when_pressed(self, informations):
        current = self.equation.text
        #czyszczenie
        if informations.text == 'AC':
            self.first = True
            self.last = True
            self.equation.text = ''

        elif informations.text == '':
            pass
        
        #działania
        elif informations.text in self.actions: 
            if self.first == False:
                #otrzymywanie wyniku
                if informations.text == '=':
                    if self.last == False:
                        self.last = True
                        self.was = False
                        new_text = current + informations.text
                        self.equation.text = new_text
                        self.count()
                #działania
                else:
                    if self.last == False and self.was == False:
                        self.last = True
                        self.was = True
                        new_text = current + informations.text
                        self.equation.text = new_text
        #liczby
        else:
            self.first = False
            self.last = False
            if self.counted == True:
                current = ''
                self.counted = False
            new_text = current + informations.text
            self.equation.text = new_text



    def add(x, a, b):
        return a + b
    def odd(x, a, b):
        return a - b
    def multiply(x, a, b):
        return a * b
    def divide(x, a, b):
        if b == 0:
            return False
        else:
            return a / b
    def expp(x, a, b):
        return a ** b


    def count(self):
        tab = []
        tabs = ['=']
        current = self.equation.text

        #odzczytywanie dzialania
        for i in current:
            if i in self.actions:
                tab.append(i)
            else:
                tab.append(int(i))

        #laczenie liczb
        wyk = 1
        for i in range(len(tab)-2, -1, -1): 
            if tab[i] in self.actions:
                tabs.append(tab[i])
                wyk = 1
            else:
                if tabs[len(tabs)-1] in self.actions:
                    tabs.append(tab[i]*wyk)
                    wyk = wyk * 10
                else:
                    tabs[len(tabs)-1] += tab[i]*wyk
                    wyk = wyk * 10
        #obrot
        tab = tabs[::-1]
        tabs = []

        dziel0 = False

        #obliczenia
        if tab[1] == '^':
            wynik = self.expp(tab[0], tab[2])
        elif tab[1] == '*':
            wynik = self.multiply(tab[0], tab[2])
        elif tab[1] == '/':
            if self.divide(tab[0], tab[2]) == False:
                dziel0 = True
            else:
                wynik = self.divide(tab[0], tab[2])
        elif tab[1] == '+':
            wynik = self.add(tab[0], tab[2])
        elif tab[1] == '-':
            wynik = self.odd(tab[0], tab[2])
        elif tab[1] == '=':
            wynik = tab[0]
        

        self.counted = True

        #wypisywanie wyniku
        if dziel0 == True:
            self.equation.text = 'BŁĄD! Dzielenie przez 0!'
        else:
            new_text = current + str(wynik)
            self.equation.text = new_text

        

#inicjacja kalkulatora
if __name__ == '__main__':
    app = MyApp()
    app.run()