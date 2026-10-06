# Python'da `main()` funksiyasi va `if __name__ == '__main__'` — Dastur kirish nuqtasi (Entry Point)

## Mundarija

1. Kirish va rasmdagi kod
2. Nazariya: `__name__` nima?
3. Python faylni qanday bajaradi?
4. Pseudocode
5. Amaliy tajriba: run vs import
6. Nega `main()` funksiyasi kerak?
7. `main()` ning kengaytirilgan shakli (`argparse`, `sys.exit`)
8. Boshqa tillarda kirish nuqtasi (C, C++, Java)
9. Complexity tahlili
10. Ko'p uchraydigan xatolar
11. Best practices
12. Mashqlar
13. Xulosa

---

## 1. Kirish va rasmdagi kod

Rasmdagi kod Python dasturlarining eng keng tarqalgan **shablonidir**:

```python
def main():
    # Код и логика здесь...
    # ...

# Точка входа в программу
if __name__ == '__main__':
    main()
```

Izohlarning tarjimasi:

- `# Код и логика здесь...` → "Kod va mantiq shu yerda..."
- `# Точка входа в программу` → "Dasturning kirish nuqtasi (entry point)"

Bu shablon ikki qismdan iborat:

| Qism | Vazifasi |
|------|----------|
| `def main():` | Dasturning asosiy mantiqini bitta funksiyaga o'raydi |
| `if __name__ == '__main__':` | Fayl **to'g'ridan-to'g'ri ishga tushirilganda** `main()` ni chaqiradi, **import** qilinganda esa chaqirmaydi |

**Asosiy g'oya:** bitta `.py` fayl ham *dastur* (script), ham *kutubxona* (module) sifatida ishlata olishi kerak.

---

## 2. Nazariya: `__name__` nima?

### 2.1. Module tushunchasi

Python'da har bir `.py` fayl — bu **module**. Fayl nomi `utils.py` bo'lsa, module nomi `utils` bo'ladi.

### 2.2. `__name__` — maxsus (dunder) o'zgaruvchi

`__name__` — Python interpreter har bir module uchun avtomatik yaratadigan **global o'zgaruvchi**. ("dunder" = **d**ouble **under**score, ya'ni ikki tomondan pastki chiziq.)

Uning qiymati faylning **qanday ishga tushirilganiga** bog'liq:

| Holat | `__name__` qiymati |
|-------|--------------------|
| Fayl to'g'ridan-to'g'ri ishga tushirilsa: `python file.py` | `'__main__'` |
| Fayl boshqa joydan import qilinsa: `import file` | `'file'` (module nomi) |

### 2.3. Nima uchun aynan `'__main__'`?

Python ishga tushganda, birinchi bajarilayotgan faylni **top-level script environment** deb ataydi va uning nomini `'__main__'` qilib belgilaydi. Shuning uchun:

```python
if __name__ == '__main__':
```

o'qilishi: **"Agar bu fayl asosiy (birinchi ishga tushirilgan) fayl bo'lsa..."**

---

## 3. Python faylni qanday bajaradi?

Bu — eng muhim tushuncha. Python **yuqoridan pastga, qatorma-qator** bajaradi. `def` ham bajariladigan statement: u funksiya obyektini yaratadi va nomga bog'laydi, lekin **funksiya tanasini bajarmaydi**.

Quyidagi fayl uchun:

```python
print("1) Fayl boshlandi")

def main():
    print("3) main() ichida")

print("2) def dan keyin")

if __name__ == '__main__':
    main()
```

Natija (`python file.py`):

```
1) Fayl boshlandi
2) def dan keyin
3) main() ichida
```

Diqqat: `def main()` ni ko'rganda Python faqat funksiyani **eslab qoladi**. `main()` faqat pastdagi `if` shartida chaqirilgandagina ishlaydi.

### Import qilinganda nima bo'ladi?

`import file` yozilganda Python faylni **butunlay bir marta bajaradi** (yuqoridan pastga). Bu paytda `__name__ == 'file'` bo'ladi, shuning uchun `if` sharti `False` bo'ladi va `main()` chaqirilmaydi.

---

## 4. Pseudocode

### 4.1. Python interpreter mantig'i (soddalashtirilgan)

```
FUNCTION run_python_file(path, as_script):
    CREATE new module namespace M

    IF as_script THEN
        M.__name__ ← "__main__"
    ELSE
        M.__name__ ← module_name_from(path)
    END IF

    FOR EACH statement IN parse(path) DO
        execute statement IN namespace M
    END FOR
END FUNCTION
```

### 4.2. Shablonimiz pseudocode'da

```
DEFINE main():
    // asosiy mantiq
END DEFINE

IF __name__ = "__main__" THEN
    CALL main()
END IF
```

### 4.3. Qaror daraxti

```
Fayl ishga tushdi
        │
        ▼
 Qanday ishga tushdi?
   │              │
 python file.py  import file
   │              │
   ▼              ▼
__name__ =     __name__ =
"__main__"      "file"
   │              │
   ▼              ▼
main() CHAQIRILADI   main() CHAQIRILMAYDI
                     (faqat funksiyalar
                      e'lon qilinadi)
```

---

## 5. Amaliy tajriba: run vs import

Ikkita fayl yaratamiz.

### `calculator.py`

```python
def add(a, b):
    return a + b


def main():
    print("Calculator ishga tushdi")
    print("2 + 3 =", add(2, 3))


print("calculator.py: __name__ =", __name__)

if __name__ == '__main__':
    main()
```

### `app.py`

```python
import calculator

print("app.py: __name__ =", __name__)
print("10 + 5 =", calculator.add(10, 5))
```

### 1-tajriba: `calculator.py` ni to'g'ridan-to'g'ri ishga tushirish

```bash
python calculator.py
```

```
calculator.py: __name__ = __main__
Calculator ishga tushdi
2 + 3 = 5
```

### 2-tajriba: `app.py` ni ishga tushirish

```bash
python app.py
```

```
calculator.py: __name__ = calculator
app.py: __name__ = __main__
10 + 5 = 15
```

Ko'ryapsizmi: `calculator.py` import qilinganda uning `__name__` qiymati `'calculator'` bo'ldi va `main()` **ishlamadi**. Faqat `add()` funksiyasidan foydalandik. Aynan shu uchun biz ushbu shablonni ishlatamiz.

### Agar shablon bo'lmasa-chi?

```python
# calculator_bad.py
def add(a, b):
    return a + b

print("Calculator ishga tushdi")   # <-- himoyasiz kod
print("2 + 3 =", add(2, 3))
```

Endi `import calculator_bad` yozsangiz — **istalmagan** `print` lar ham bajariladi. Katta loyihada bu: sekinlashish, xato yon ta'sirlar (side effects), tasodifiy fayl yozish, tarmoqqa so'rov yuborish kabi muammolarga olib keladi.

---

## 6. Nega `main()` funksiyasi kerak?

Faqat `if __name__ == '__main__':` ning ichiga barcha kodni yozish ham mumkin. Lekin `main()` funksiyasi bir nechta afzallik beradi.

### 6.1. Global scope'ni ifloslantirmaydi

`if __name__ == '__main__':` bloki **global scope** da joylashgan. U yerda yaratilgan o'zgaruvchilar global bo'ladi:

```python
# Yomon
if __name__ == '__main__':
    x = 10
    result = x * 2
    print(result)

def foo():
    print(x)   # x global — kutilmagan holatda ishlab ketadi!
```

`main()` ichida esa o'zgaruvchilar **local** bo'ladi:

```python
# Yaxshi
def main():
    x = 10
    result = x * 2
    print(result)

if __name__ == '__main__':
    main()
```

### 6.2. Test qilish oson

`main()` — oddiy funksiya, uni test fayldan chaqirish mumkin:

```python
# test_app.py
import app

def test_main_runs():
    app.main()   # xatosiz ishlashi kerak
```

`if __name__` blokining ichidagi kodni esa import orqali test qilib bo'lmaydi.

### 6.3. Qayta ishlatish (reusability)

```python
import app

app.main()   # boshqa dasturdan chaqirish mumkin
```

### 6.4. Tuzilish va o'qilishi

Kod o'quvchi (yoki siz o'zingiz 3 oydan keyin) darhol tushunadi: *"Dastur shu yerdan boshlanadi"*.

### 6.5. Tezlik haqida eslatma

Funksiya ichidagi **local** o'zgaruvchilarga murojaat CPython'da global o'zgaruvchilarga qaraganda biroz tezroq (`LOAD_FAST` vs `LOAD_GLOBAL`). Katta tsikllarda bu sezilarli bo'lishi mumkin.

---

## 7. `main()` ning kengaytirilgan shakli

Real loyihalarda shablon odatda quyidagicha ko'rinadi:

```python
import argparse
import sys


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Namuna dastur")
    parser.add_argument("name", help="Foydalanuvchi ismi")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Batafsil chiqish")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    if args.verbose:
        print("Verbose rejim yoqildi")

    print(f"Salom, {args.name}!")
    return 0          # 0 = muvaffaqiyat


if __name__ == '__main__':
    sys.exit(main())
```

Ishga tushirish:

```bash
python greet.py Zafar -v
```

```
Verbose rejim yoqildi
Salom, Zafar!
```

### Nima uchun `sys.exit(main())`?

- `main()` **exit code** (int) qaytaradi.
- `0` — muvaffaqiyat, `0` dan farqli son — xato.
- Operatsion tizim va boshqa dasturlar (shell, CI/CD, `make`) shu kod orqali dastur muvaffaqiyatli tugaganini bilib oladi.

```bash
python greet.py Zafar
echo $?        # oxirgi dastur exit code'ini ko'rsatadi
```

### `main(argv=None)` nima uchun?

Argumentlarni parametr sifatida berish testni osonlashtiradi:

```python
def test_greet():
    assert main(["Zafar"]) == 0
```

---

## 8. Boshqa tillarda kirish nuqtasi (Entry Point)

Python'da kirish nuqtasi **konventsiya** (kelishuv). Boshqa ko'p tillarda esa u **tilning o'zi talab qiladi**.

### 8.1. Python

```python
def main():
    print("Salom, dunyo!")

if __name__ == '__main__':
    main()
```

### 8.2. C

```c
#include <stdio.h>

int main(void) {
    printf("Salom, dunyo!\n");
    return 0;
}
```

- `main` — **majburiy**. Linker aynan shu nomni qidiradi.
- `return 0` — exit code (Python'dagi `sys.exit(0)` ga o'xshash).

### 8.3. C++

```cpp
#include <iostream>

int main() {
    std::cout << "Salom, dunyo!\n";
    return 0;
}
```

### 8.4. Java

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Salom, dunyo!");
    }
}
```

### 8.5. Taqqoslash jadvali

| Til | Kirish nuqtasi | Majburiymi? | Import qilganda ishlaydimi? |
|-----|----------------|-------------|------------------------------|
| C / C++ | `int main()` | Ha (linker talab qiladi) | Import tushunchasi yo'q (`#include` faqat e'lon) |
| Java | `public static void main(String[])` | Ha (JVM talab qiladi) | Faqat ishga tushirilgan class'ning `main` i |
| Python | `if __name__ == '__main__'` | **Yo'q** (konventsiya) | Himoya bo'lmasa — hammasi bajariladi |

**Muhim farq:** C, C++ va Java'da `main` — bu *dastur* va *kutubxona* ni ajratadi. Python'da `if __name__ == '__main__'` ham xuddi shu vazifani bajaradi.

---

## 9. Complexity tahlili

| Operatsiya | Vaqt | Izoh |
|-----------|------|------|
| `__name__ == '__main__'` taqqoslash | **O(1)** | Ikkita string'ni taqqoslash (qisqa, o'zgarmas uzunlik) |
| `main()` ni chaqirish (overhead) | **O(1)** | Funksiya chaqirish — doimiy narx |
| `def main()` e'lon qilish | **O(1)** | Faqat funksiya obyektini yaratish |
| `main()` ichidagi mantiq | Sizning algoritmingizga bog'liq | Masalan, O(n log n) |

**Xotira:** `main()` frame uchun O(1) qo'shimcha xotira, local o'zgaruvchilar esa algoritmga bog'liq.

**Xulosa:** shablonning o'zi samaradorlikka **deyarli ta'sir qilmaydi**; afzalliklari — toza kod, xavfsiz import va test qilish osonligi.

**Import-time xarajat:** module import qilinganda uning **barcha top-level kodi** bajariladi. Shuning uchun og'ir hisob-kitoblar (fayl o'qish, tarmoq, katta tsikllar) top-level'da emas, funksiya ichida bo'lishi kerak.

---

## 10. Ko'p uchraydigan xatolar

### Xato 1: `main()` ni e'lon qilib, chaqirishni unutish

```python
def main():
    print("Salom")
# hech narsa chiqmaydi!
```

### Xato 2: Qavs yozishni unutish

```python
if __name__ == '__main__':
    main        # funksiya chaqirilmaydi, faqat nomga murojaat
```

To'g'ri: `main()`.

### Xato 3: Noto'g'ri yozilgan dunder

```python
if _name_ == '_main_':      # NameError — bitta pastki chiziq
if __name__ == '__main__':  # to'g'ri — IKKITA pastki chiziq
```

### Xato 4: Qo'shtirnoq ichidagi `__main__` ni o'zgartirish

```python
if __name__ == '__Main__':   # katta-kichik harf muhim! Hech qachon ishlamaydi
```

### Xato 5: Shartdan oldin hamma narsani top-level'da yozish

```python
data = load_huge_file()      # import qilinganda ham ishlaydi!
def main(): ...
```

Yechim: `load_huge_file()` ni `main()` ichiga ko'chiring.

### Xato 6: `main()` da global o'zgaruvchiga yozishni urinish

```python
counter = 0

def main():
    counter += 1   # UnboundLocalError!
```

Yechim: `global counter` ishlating yoki (yaxshisi) o'zgaruvchini parametr sifatida uzating.

### Xato 7: Circular import

Ikkita fayl bir-birini import qilsa va top-level'da kod bajarsa, xato chiqishi mumkin. `main()` ga o'rash bu muammoni kamaytiradi.

---

## 11. Best practices

1. **Doim** `main()` funksiyasidan foydalaning, hatto kichik skriptlarda ham.
2. `main()` imkon qadar **qisqa** bo'lsin — u boshqa funksiyalarni chaqiruvchi "dirijyor" bo'lsin.
3. Exit code qaytaring: `sys.exit(main())`.
4. `argv` ni parametr sifatida qabul qiling (test uchun).
5. Top-level'da faqat: `import`, konstantalar, `def`/`class` e'lonlari.
6. Python 3.x da `main()` ga type hint qo'shing: `def main() -> int:`.
7. Paket (package) uchun `__main__.py` fayli ham mavjud: `python -m mypackage` buyrug'i shu faylni ishga tushiradi.

---

## 12. Mashqlar

### Mashq 1 (oson)
Quyidagi kod nima chiqaradi? `python a.py` va `import a` holatlari uchun alohida javob bering.

```python
print("A")

def f():
    print("B")

if __name__ == '__main__':
    print("C")
    f()
```

<details>
<summary>Javob</summary>

- `python a.py` → `A`, `C`, `B`
- `import a` → faqat `A`

</details>

### Mashq 2 (o'rta)
`stats.py` module yarating: `mean(lst)` va `median(lst)` funksiyalari bo'lsin. Fayl to'g'ridan-to'g'ri ishga tushirilganda `[1, 2, 3, 4, 10]` ro'yxati uchun natijani chop etsin. Boshqa faylda import qilib, faqat funksiyalardan foydalaning.

### Mashq 3 (o'rta)
`argparse` yordamida dastur yozing: `python tool.py 5 --square` → `25`; `python tool.py 5` → `5`. Exit code qaytaring.

### Mashq 4 (qiyin)
`print(__name__)` ni quyidagi 3 usulda ishga tushirib, natijani tushuntiring:

```bash
python file.py
python -c "import file"
python -m file
```

<details>
<summary>Javob</summary>

1. `__main__`
2. `file`
3. `__main__` (`-m` bilan module script sifatida ishga tushiriladi)

</details>

### Mashq 5 (tahlil)
Nima uchun C'da `if __name__ == '__main__'` ga o'xshash konstruksiya kerak emas? Linker va `#include` ning ishlash tamoyilini o'ylab tushuntiring.

---

## 13. Xulosa

| Tushuncha | Qisqacha |
|-----------|----------|
| `__name__` | Har bir module uchun interpreter yaratadigan o'zgaruvchi |
| `'__main__'` | Fayl to'g'ridan-to'g'ri ishga tushirilganda `__name__` ning qiymati |
| `main()` | Dasturning asosiy mantiqini o'rab turuvchi funksiya |
| Shablon maqsadi | Fayl ham dastur, ham kutubxona sifatida xavfsiz ishlashi |
| Afzalliklari | Toza scope, test qilish osonligi, qayta ishlatish, import xavfsizligi |
| Murakkablik | O(1) qo'shimcha xarajat |

**Eslab qoling:**

> Kod **import** qilinganda — faqat *e'lon qilinadi*.
> Kod **run** qilinganda — *e'lon qilinadi va ishga tushadi*.

Shablon aynan shu farqni boshqaradi:

```python
def main():
    ...

if __name__ == '__main__':
    main()
```

---

## Qo'shimcha manbalar

- Python rasmiy hujjati: `__main__` — Top-level code environment
- Python rasmiy hujjati: `argparse` — Command-line parsing
- PEP 8 — Python Style Guide
