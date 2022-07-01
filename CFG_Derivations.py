import streamlit as st
from collections import defaultdict
import random
import requests
from streamlit_lottie import st_lottie


st.set_page_config(layout="centered", initial_sidebar_state="auto")


class CFG(object):

    def __init__(self):
        self.prod = defaultdict(list)
        self.win = 'S=> '
        self.count = 0
        self.current = ''

    def add_prod(self, lhs, rhs):
        prods = rhs.split('|')  # Eg: ['a S b'], ['a S a']...
        if prods == ['^']:
            prods = [' ']
        for prod in prods:
            # Eg: [('a', 'S', 'b')], [('a', 'S', 'b'), ('a', 'S', 'a')]
            self.prod[lhs].append(tuple(prod.split()))

    def gen_random_left(self, symbol):
        # Generate a random sentence from the grammar, starting with the given symbol
        sentence = ''
        # select one production of that start with symbol randomly
        rand_prod = random.choice(self.prod[symbol])
        # print(rand_prod)
        rule = (str(rand_prod).replace(',', '').replace(
            '\'', '').replace('(', '').replace(')', '').replace(' ', ''))
        # print(rule)
        self.replace_left(rule)
        for sym in rand_prod:
            # for non-terminals, recurse
            if sym in self.prod:
                sentence += self.gen_random_left(sym)
            else:
                sentence += sym + ' '
        return sentence

    def replace_left(self, rule):
        # store current rule, print
        # on next iteration: search the rule, replace instances of CAPITAL letters with the new rule
        if self.count < 1:
            self.current = rule
        else:
            for c in self.current:
                if c.isupper():
                    self.current = self.current.replace(c, rule, 1)
                    break
        self.win = self.win+self.current+' => '
        self.count = self.count + 1

    def gen_random_right(self, symbol):
        sentence = ''
        cap = 0
        # select one production of that start with symbol randomly
        rand_prod = random.choice(self.prod[symbol])
        rule = (str(rand_prod).replace(',', '').replace(
            '\'', '').replace('(', '').replace(')', '').replace(' ', ''))
        for sym in rule:
            if sym.isupper():  # calculating the number of Capital Letters/Non-terminals in the Rule
                cap += 1

        if(cap > 1):
            self.replace_right()(rule[::-1], cap)
            for sym in reversed(rand_prod):
                # for non-terminals, recurse
                if sym in self.prod:
                    sentence += self.gen_random_right(sym)
                else:
                    sentence += sym + ' '
            return sentence[::-1]
        elif(cap == 1):
            self.replace_left(rule)
            for sym in rand_prod:
                # for non-terminals, recurse
                if sym in self.prod:
                    sentence += self.gen_random_left(sym)
                else:
                    sentence += sym + ' '
            return sentence
        else:
            self.replace_right()(rule, cap)
            for sym in (rand_prod):
                # for non-terminals, recurse
                if sym in self.prod:
                    sentence += self.gen_random_right(sym)
                else:
                    sentence += sym + ' '
            return sentence

    def replace_right(self, rule, cap):
        if self.count < 1:
            self.current = rule  # AB
        else:
            for c in self.current:  # AB
                if c.isupper():
                    self.current = (self.current).replace(c, rule, 1)  # aaB
                    break
        cap1 = 0
        for sym in self.current:
            if sym.isupper():
                cap1 += 1  # 3,2,1
        if(cap1 >= 0):
            self.win = self.win+self.current[::-1]+' => '  # S=>BA=>Baa=>Abbaa
        else:
            self.win = self.win+self.current+' => '
        self.count = self.count + 1

    def clearString(self):
        self.win = 'S=> '
        self.count = 0
        self.current = ''


def main():
    # pg = st.sidebar.radio("", ['Home'])

    # if pg == 'Home':
    text_display = '<h1 style="font-family:Sans-serif; color:#00BCD0;">Simulate Derivations of Context-Free Grammar</h1>'
    st.markdown(text_display, unsafe_allow_html=True)
    # st.write("### Simulate Derivations of Context-Free Grammar")
    text_display = '<p style="font-family:Sans-serif; color:#BBBBBB; font-size: 20px">This project checks if an input string is part of the language by performing Leftmost Derivation and Rightmost Derivation based on the users choice.</p>'
    st.markdown(text_display, unsafe_allow_html=True)

    st.title("Simulating Context-Free Grammar")
    st.write("### Enter Production Rules")

    text_display = '<p style="font-family:Sans-serif; color:#74bed6; font-size: 15px">Production rules must be entered in the specified format. For Example: S -> aSb <br> While giving the Production rules, space must be given before and after the arrow(->)</p>'
    # text_display = '<p style="font-family:Sans-serif; color:#74bed6; font-size: 15px"> </p>'
    st.markdown(text_display, unsafe_allow_html=True)

    def load_lottieurl(url):
     r = requests.get(url)
     if r.status_code != 200:
        return None
     return r.json()
    lottie_coding = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_zw1coqqh.json")

    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            s = st.number_input("Number of Rules", format="%d", step=1)

            f = open('ProductionRules.txt', 'w')
            for i in range(s):
                j = st.text_input("Rule {}:".format(i+1))
                j += '\n'
                f.write(j)
            w = st.text_input("Enter String: ")  # eg: aabbba
            w = (" ".join(w))+" "  # eg: a a b b b a a_
            f.close()

            counter = 0
            cfg1 = CFG()
            if(st.button('Submit')):
                f = open('ProductionRules.txt')
                for line in iter(f):
                    first = str(line[0])  # First Alphabet Eg: S
                    sec = str(line[5:].rstrip())  # rules. Eg: aSb
                    sec = (" ".join(sec))  # Eg: a S b
                    cfg1.add_prod(first, sec)
                    counter += 1
                f.close()

                lmd = cfg1.gen_random_left('S')
                for i in range(0, 50000):
                    if str(w.strip()) == lmd.strip():
                        break
                    cfg1.clearString()
                    lmd = cfg1.gen_random_left('S')

                if str(w.strip()) == lmd.strip():
                    text_display = '<h3 style="font-family:Sans-serif; color:#74bed6;">Leftmost Derivation:</h3>'
                    st.markdown(text_display, unsafe_allow_html=True)
                    out = str(cfg1.win+lmd).replace(' ', '').replace('(',
                                                                     '').replace(')', '').replace('=>', ' ⇒ ')
                    st.write("#### {}".format(out))
                    st.success("String exists!!!")
                    st.balloons()
                else:
                    st.write("### The String doesn't not exist in grammar")
                    st.error("Try Again")

                cfg1.clearString()
                rmd = cfg1.gen_random_right('S')
                for i in range(0, 50000):
                    if str(w.strip()) == rmd.strip():
                        break
                    cfg1.clearString()
                    rmd = cfg1.gen_random_right('S')

                if str(w.strip()) == rmd.strip():
                    text_display = '<h3 style="font-family:Sans-serif; color:#74bed6;">Rightmost Derivation:</h3>'
                    st.markdown(text_display, unsafe_allow_html=True)
                    out = str(cfg1.win+rmd).replace(' ', '').replace('(',
                                                                     '').replace(')', '').replace('=>', ' ⇒ ')
                    st.write("#### {}".format(out))
                    st.success("String exists!!!")
                    st.balloons()
                else:
                    st.write("### The String doesn't not exist in grammar")
                    st.error("Try Again")
        with right_column:
          st_lottie(lottie_coding, height=300, key="coding")

    st.write("[My Profile >](https://linktr.ee/Ankur_Raut)")

if __name__ == "__main__":
    main()
