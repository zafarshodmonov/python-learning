# Python `click` bilan CLI ilovalar yaratish

Bu darslik rasmdagi kod asosida tuzilgan. Maqsad: `click` qanday ishlashini, har bir decorator nima qilishini va nima uchun shunday yozilishini tushunish.

## 1. Maqsad va oldingi bilimlar

- Python funksiyalari, decorator'lar (`@...` sintaksisi) haqida asosiy tushuncha
- Terminal (command line) bilan ishlash tajribasi

Darsdan keyin siz:

1. `click` da **group**, **command**, **option**, **argument** farqini bilasiz
2. O'zingizning ko'p buyruqli (subcommand) CLI ilovangizni yozasiz
3. `click` ni `argparse` va `typer` bilan solishtira olasiz

---

## 2. Kod

```python
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.argument('name')
def hello(count, name):
    for x in range(count):
        click.echo(f"Hello {name}!")

if __name__ == '__main__':
    cli()

# $ python app.py hello John
# Hello John!

# $ python app.py hello Kate --count=3
# Hello Kate!
# Hello Kate!
# Hello Kate!
```

---

## 3. Nazariya: CLI ilova qanday qismlardan iborat?

Quyidagi buyruqni ko'rib chiqing:

```
python app.py hello Kate --count=3
```

| Qism | Nomi | Vazifasi |
|---|---|---|
| `python app.py` | dastur | Ilovani ishga tushiradi |
| `hello` | **subcommand** | Qaysi amalni bajarish kerakligini tanlaydi |
| `Kate` | **argument** (positional) | Majburiy qiymat, o'rniga qarab aniqlanadi |
| `--count=3` | **option** (flag) | Ixtiyoriy qiymat, nomi bilan beriladi |

**Asosiy farq: argument va option**

- **Argument**: odatda majburiy, nomi yozilmaydi (`Kate`)
- **Option**: odatda ixtiyoriy, `--nom` bilan beriladi, `default` qiymati bo'ladi

---

## 4. Kodni qatorma-qator tahlil

### 4.1. `@click.group()`

```python
@click.group()
def cli():
    pass
```

- `cli` funksiyasi **Group** obyektiga aylanadi. Group bu subcommand'lar uchun "konteyner".
- `git` ni eslang: `git` (group), `git commit`, `git push` (subcommand'lar). Bu yerda ham xuddi shunday.
- Funksiya tanasi (`pass`) bo'sh, chunki group'ning o'zi hech narsa qilmaydi. Lekin u yerga umumiy sozlamalarni (masalan, `--verbose`) qo'yish mumkin.

> **Muhim:** `cli` endi oddiy funksiya emas. `cli()` chaqirilganda click `sys.argv` ni o'qiydi va kerakli subcommand'ni topadi.

### 4.2. `@cli.command()`

```python
@cli.command()
def hello(...):
```

- `hello` funksiyasini `cli` group'iga **subcommand** sifatida ro'yxatdan o'tkazadi.
- Buyruq nomi funksiya nomidan olinadi: `hello`.
- Boshqa nom berish uchun: `@cli.command(name="salom")`.

### 4.3. `@click.option('--count', default=1, help='...')`

- `--count` ixtiyoriy parametr.
- `default=1`: berilmasa 1 bo'ladi.
- **Tur (type) avtomatik aniqlanadi:** `default=1` int bo'lgani uchun click `--count=3` ni `int` ga o'giradi. `--count=abc` desa, xato beradi.
- `help=`: `--help` da ko'rinadigan tavsif.
- Funksiya parametri nomi `count`, chunki `--count` dan `--` olib tashlanadi (`--dry-run` bo'lsa, `dry_run` bo'ladi).

### 4.4. `@click.argument('name')`

- Majburiy **positional** parametr.
- Berilmasa, click xato chiqaradi:

```
Usage: app.py hello [OPTIONS] NAME
Error: Missing argument 'NAME'.
```

### 4.5. `def hello(count, name)`

- click qiymatlarni funksiyaga **nomi bo'yicha** (keyword) uzatadi, tartibi bo'yicha emas. Shuning uchun `(count, name)` yoki `(name, count)` bo'lishi farq qilmaydi.
- Decorator'lar tartibi faqat `--help` dagi ko'rinishga va argument'lar o'rniga ta'sir qiladi.

### 4.6. `click.echo(...)`

- `print` ga o'xshaydi, lekin Python 2/3, Windows/Linux va turli encoding'larda xavfsizroq ishlaydi.
- Pipe qilinganda (`| less`) rangli matnni avtomatik olib tashlaydi.
- Xatoni stderr ga yozish: `click.echo("xato", err=True)`.

### 4.7. `if __name__ == '__main__': cli()`

- Fayl to'g'ridan-to'g'ri ishga tushirilganda `cli()` chaqiriladi.
- `cli()` ichida click argv ni o'qiydi, parse qiladi va tegishli funksiyani chaqiradi. Funksiya tugagach, dastur `sys.exit()` bilan chiqadi.

---

## 5. Pseudocode: click ichida nima sodir bo'ladi?

```
FUNCTION cli_main(argv):
    tokens ← argv[1:]

    // 1. Group darajasidagi option'lar (bu misolda yo'q)
    parse_options(group, tokens)

    // 2. Subcommand'ni topish
    name ← tokens.pop_first_positional()
    IF name NOT IN group.commands:
        error("No such command"); exit(2)
    command ← group.commands[name]

    // 3. Subcommand parametrlarini ajratish
    values ← {}
    FOR EACH param IN command.params:
        IF param is option:
            raw ← find "--nom" in tokens ELSE param.default
        ELSE IF param is argument:
            raw ← take next positional from tokens
            IF raw IS MISSING: error("Missing argument"); exit(2)
        values[param.name] ← convert(raw, param.type)
            // convert xato bersa → error; exit(2)

    // 4. Chaqirish
    group.callback()                 // cli() tanasi
    command.callback(**values)       // hello(count=..., name=...)
```

---

## 6. Murakkablik tahlili

`t` = argv dagi token'lar soni, `p` = parametrlar soni, `c` = `--count` qiymati.

| Bosqich | Murakkablik |
|---|---|
| Argv ni parse qilish | O(t) |
| Subcommand'ni qidirish (dict) | O(1) |
| Parametrlarni moslashtirish | O(p) |
| `hello` ichidagi sikl | O(c) |
| **Jami** | **O(t + p + c)** |

Amalda parse vaqti ahamiyatsiz, asosiy vaqt funksiya ichidagi ishga ketadi.

---

## 7. Ishga tushirish va natijalar

```bash
pip install click
```

| Buyruq | Natija |
|---|---|
| `python app.py hello John` | `Hello John!` |
| `python app.py hello Kate --count=3` | `Hello Kate!` (3 marta) |
| `python app.py hello Kate --count 3` | Xuddi shu (probel bilan ham bo'ladi) |
| `python app.py hello` | `Error: Missing argument 'NAME'.` (exit code 2) |
| `python app.py hello Kate --count=abc` | `Error: Invalid value for '--count'` |
| `python app.py --help` | Group yordami: mavjud buyruqlar ro'yxati |
| `python app.py hello --help` | `hello` yordami: option va argument'lar |

`--help` ni click **avtomatik** yaratadi. Qo'lda yozish shart emas.

---

## 8. Boshqa kutubxonalar bilan implementatsiya

### 8.1. `argparse` (standart kutubxona)

```python
import argparse

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    hello = sub.add_parser("hello", help="Greet someone")
    hello.add_argument("name")
    hello.add_argument("--count", type=int, default=1,
                       help="Number of greetings.")

    args = parser.parse_args()

    if args.command == "hello":
        for _ in range(args.count):
            print(f"Hello {args.name}!")

if __name__ == "__main__":
    main()
```

### 8.2. `typer` (type hint'larga asoslangan, click ustiga qurilgan)

```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str, count: int = 1):
    for _ in range(count):
        typer.echo(f"Hello {name}!")

if __name__ == "__main__":
    app()
```

> Typer'da bitta command bo'lsa, `hello` nomi yozilmaydi (`python app.py John`). Group kabi ishlashi uchun kamida ikkita command kerak.

### 8.3. Solishtirish

| Mezon | `argparse` | `click` | `typer` |
|---|---|---|---|
| O'rnatish | Kerak emas | `pip install click` | `pip install typer` |
| Sintaksis | Imperativ (`add_argument`) | Decorator | Type hint |
| Subcommand | `add_subparsers` (og'irroq) | `@group` + `@command` (qulay) | `@app.command()` |
| Tur aniqlash | `type=` | `default` yoki `type=` | Annotation'dan |
| Kod hajmi | Ko'proq | O'rtacha | Eng kam |
| Yaxshi tomoni | Qo'shimcha dependency yo'q | Pishgan, ko'p imkoniyat | Eng qisqa |

---

## 9. Ko'p uchraydigan xatolar

1. **Decorator'ni unutish:** `@cli.command()` yo'q bo'lsa, `hello` subcommand sifatida ko'rinmaydi.
2. **Parametr nomi mos kelmaydi:** `@click.option('--count')` bo'lsa, funksiyada `count` bo'lishi kerak, aks holda `TypeError`.
3. **`cli()` o'rniga `cli`:** `if __name__` blokida qavs unutilsa, hech narsa ishlamaydi.
4. **`default=1` va tur:** `default="1"` yozsangiz, tur `str` bo'lib qoladi. Aniq berish uchun `type=int`.
5. **Argument va option'ni aralashtirish:** `@click.argument('--name')` xato. Argument nomida `--` bo'lmaydi.

---

## 10. Foydali imkoniyatlar (keyingi qadamlar)

```python
@click.command()
@click.option('--name', prompt='Ismingiz',
              help='Foydalanuvchi ismi.')                 # so'raydi
@click.option('--lang', type=click.Choice(['uz', 'en']),
              default='uz')                               # tanlov cheklovi
@click.option('--verbose', '-v', is_flag=True)            # flag (True/False)
@click.argument('files', nargs=-1,
                type=click.Path(exists=True))             # ko'p fayl
def run(name, lang, verbose, files):
    ...
```

- `prompt=True`: qiymat berilmasa, terminalda so'raydi
- `click.Choice([...])`: faqat ruxsat etilgan qiymatlar
- `is_flag=True`: qiymatsiz flag (`--verbose`)
- `nargs=-1`: cheksiz sondagi argument
- `click.Path(exists=True)`: fayl mavjudligini tekshiradi
- `envvar='MY_VAR'`: qiymatni environment variable'dan oladi

---

## 11. Mashqlar

1. `hello` ga `--upper` flag qo'shing: berilsa, matn katta harflarda chiqsin.
2. `goodbye` nomli ikkinchi subcommand yozing (`Goodbye {name}!`).
3. `--lang` option qo'shing (`uz` → `Salom`, `en` → `Hello`), `click.Choice` ishlating.
4. Group'ga `--verbose` option qo'shing va subcommand ichida undan foydalaning (maslahat: `@click.pass_context` va `ctx.obj`).
5. Xuddi shu dasturni `argparse` da qayta yozib, kod hajmini solishtiring.

### Mashq 1 yechimi

```python
@cli.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--upper', is_flag=True, help='Print in uppercase.')
@click.argument('name')
def hello(count, upper, name):
    msg = f"Hello {name}!"
    if upper:
        msg = msg.upper()
    for _ in range(count):
        click.echo(msg)
```

---

## 12. Qisqacha xulosa

- `@click.group()` buyruqlar to'plamini yaratadi
- `@group.command()` unga subcommand qo'shadi
- `@click.option` ixtiyoriy, `@click.argument` majburiy parametr
- Qiymatlar funksiyaga **nomi bo'yicha** uzatiladi
- `--help`, tur tekshiruvi va xato xabarlarini click o'zi beradi
- Oxirida `cli()` chaqirilishi shart
