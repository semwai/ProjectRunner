--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

-- Started on 2023-05-11 22:02:20 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: root
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO root;

--
-- TOC entry 842 (class 1247 OID 16387)
-- Name: Access; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public."Access" AS ENUM (
    'user',
    'admin'
);


ALTER TYPE public."Access" OWNER TO root;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16392)
-- Name: page; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.page (
    id integer NOT NULL,
    name character varying,
    short_description character varying,
    description character varying,
    version character varying,
    container character varying NOT NULL,
    visible boolean,
    ui json,
    scenario json
);


ALTER TABLE public.page OWNER TO root;

--
-- TOC entry 214 (class 1259 OID 16391)
-- Name: page_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.page_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.page_id_seq OWNER TO root;

--
-- TOC entry 3355 (class 0 OID 0)
-- Dependencies: 214
-- Name: page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.page_id_seq OWNED BY public.page.id;


--
-- TOC entry 219 (class 1259 OID 16412)
-- Name: project; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.project (
    id integer NOT NULL,
    name character varying,
    description character varying,
    public boolean,
    content json
);


ALTER TABLE public.project OWNER TO root;

--
-- TOC entry 218 (class 1259 OID 16411)
-- Name: project_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_id_seq OWNER TO root;

--
-- TOC entry 3356 (class 0 OID 0)
-- Dependencies: 218
-- Name: project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.project_id_seq OWNED BY public.project.id;


--
-- TOC entry 217 (class 1259 OID 16403)
-- Name: user; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    name character varying,
    email character varying,
    access public."Access"
);


ALTER TABLE public."user" OWNER TO root;

--
-- TOC entry 216 (class 1259 OID 16402)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO root;

--
-- TOC entry 3357 (class 0 OID 0)
-- Dependencies: 216
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- TOC entry 3191 (class 2604 OID 16395)
-- Name: page id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.page ALTER COLUMN id SET DEFAULT nextval('public.page_id_seq'::regclass);


--
-- TOC entry 3193 (class 2604 OID 16415)
-- Name: project id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.project ALTER COLUMN id SET DEFAULT nextval('public.project_id_seq'::regclass);


--
-- TOC entry 3192 (class 2604 OID 16406)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 3345 (class 0 OID 16392)
-- Dependencies: 215
-- Data for Name: page; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.page VALUES (1, 'Первая программа', 'Первая программа', '
Создадим первую программу на языке Go. Для написания кода нам потребуется какой-нибудь текстовый редактор. Можно взять любой редактор, например, встроенный блокнот или популярный Notepad++ или любой другой. Для трансляции исходного кода в приложение необходим компилятор.

Что в этой программе делается? Программа на языке Go определяется в виде пакетов. Программный код должен быть определен в каком-то определенном пакете. Поэтому в самом начале файла с помощью оператора package указывается, к какому пакету будет принадлежать файл. В данном случае это пакет main:

`package main`

Причем пакет должен называться именно main, так как именно данный пакет определяет исполняемый файл.

При составлении программного кода нам может потребоваться функционал из других пакетов. В Go есть множество встроенных пакетов, которые содержат код, выполняющий определенные действия. Например, в нашей программе мы будем выводить сообщение на консоль. И для этого нам нужна функция Println, которая определена в пакете fmt. Поэтому второй строкой с помощью директивы import мы подключаем этот пакет:

`import fmt`

Далее идет функция main. Это главная функция любой программы на Go. По сути все, что выполняется в программе, выполняется именно функции main.

Определение функции начинается со слова func, после которого следует название функции, то есть main. После названия функции в скобках идет перечисление параметров. Так как функция main не принимает никаких параметров, то в данном случае указываются пустые скобки.

Затем в фигурных скобках определяется тело функции main - те действия, которые собственно и выполняет функция.

`func main() {`

В нашем случае функция выводит на консоль строку "Hello Go!". Для этого применяется функция Println(), которая определена в пакете fmt. Поэтому при вызове функции вначале указывается имя пакета и через точку имя функции. А в скобках функции передается то сообщение, которое она должна выводить на консоль:

`fmt.Println("Hello Go!")`

## Компиляция и выполнение программы


go - это компилятор. Поскольку при установке путь к компилятору автоматически прописывается в переменную PATH в переменных окружения, то нам не надо указывать полный путь C:\Go\bin\go.exe, а достаточно написать просто имя приложения go. Далее идет параметр run, который говорит, что мы просто хотим выполнить программу. И в конце указывается собственно файл программы hello.go.

В итоге после выполнения на консоль будет выведено сообщение "Hello Go!".


Данная команды выполняет, но не компилирует программу в отдельный исполняемый файл. Для компиляции выполним другую команду:

`go build hello.go`

После выполнения этой команды в папке с исходным файлом появится еще один файл, который будет называться helloи который мы можем запускать. После этого опять же мы можем выполнить программу, запустив в консоли этот файл', '1', 'golang:alpine', false, '{"data": [{"name": "app", "description": "file", "type": "code", "values": [{"title": "title 1", "value": "1"}], "default": "package main\nimport \"fmt\"\n \nfunc main() {\n    fmt.Println(\"Hello Go!\")\n}", "destination": "file", "file": "app.go", "env": "", "language": "go"}]}', '{"type": "Steps", "data": [{"type": "Run", "command": "go run app.go", "stdin": true, "stdout": true, "exitCode": true, "echo": true}, {"type": "Run", "command": "ls -lah", "stdin": true, "stdout": true, "exitCode": true, "echo": true}, {"type": "Run", "command": "go build app.go", "stdin": true, "stdout": true, "exitCode": true, "echo": true}, {"type": "Run", "command": "ls -lah", "stdin": true, "stdout": true, "exitCode": true, "echo": true}, {"type": "Run", "command": "./app", "stdin": true, "stdout": true, "exitCode": true, "echo": true}]}');
INSERT INTO public.page VALUES (2, 'Переменные', 'Переменные', 'Для хранения данных в программе применяются переменные. Переменная представляет именованный участок в памяти, который может хранить некотоое значение. Для определения переменной применяется ключевое слово var, после которого идет имя переменной, а затем указывается ее тип:

`var имя_переменной тип_данных`

Имя переменной представляет произвольный идентификатор, который состоит из алфавитных и цифровых символов и символа подчеркивания. При этом первым символом должен быть либо алфавитный символ, либо символ подчеркивания. При этом имена не должны представлять одно из ключевых слов: break, case, chan, const, continue, default, defer, else, fallthrough, for, func, go, goto, if, import, interface, map, package, range, return, select, struct, switch, type, var.

## Арифметические операции

Язык Go поддерживает все основные арифметические операции, которые производятся над числами. Значения, которые участвуют в операции, называются операндами. Результатом операции также является число. Список поддерживаемых арифметических операций

- \+
- \-
- \*
- \/
- \% Возвращает остаток от деления (в этой операции могут принимать участие только целочисленные операнды)
- Постфиксный инкремент (x++). Увеличивает значение переменной на единицу
- Постфиксный декремент (x--). Уменьшает значение переменной на единицу
', '1', 'golang:alpine', false, '{"data": [{"name": "app", "description": "", "type": "code", "values": [{"title": "title 1", "value": "1"}], "default": "package main\nimport \"fmt\"\n \nfunc main() {\n    var a = 4\n    var b = 6\n    var c = a - b\n    fmt.Println(c)      // -2\n}", "destination": "file", "file": "app.go", "env": "", "language": "go"}]}', '{"type": "Steps", "data": [{"type": "Run", "command": "go run app.go", "stdin": true, "stdout": true, "exitCode": true, "echo": true}]}');
INSERT INTO public.page VALUES (3, 'defer и panic', 'defer и panic', '## defer

Оператор defer позволяет выполнить определенную функцию в конце программы, при этом не важно, где в реальности вызывается эта функция. Например:

```
package main
import "fmt"

func main() {
    defer finish()
    fmt.Println("Program has been started")
    fmt.Println("Program is working")
}

func finish(){
    fmt.Println("Program has been finished")
}
```

Здесь функция finish вызывается с оператором defer, поэтому данная функция в реальности будет вызываться в самом конце выполнения программы, несмотря на то, что ее вызов определен в начале функции main

## panic

Оператору panic мы можем передать любое сообщение, которое будет выводиться на консоль. Например, в данном случае в функции divide, если второй параметр равен 0, то осуществляется вызов panic("Division by zero!").

В функции main в вызове fmt.Println(divide(4, 0)) будет выполняться оператор panic, поскольку второй параметр функции divide равен 0. И в этом случае все последующие операции, которые идут после этого вызова, например, в данном случае это вызов fmt.Println("Program has been finished"), не будут выполняться. В этом случае мы получим следующий консольный вывод:', '1', 'golang:alpine', false, '{"data": [{"name": "123", "description": "", "type": "code", "values": [{"title": "title 1", "value": "1"}], "default": "package main\nimport \"fmt\"\n \nfunc main() {\n    fmt.Println(divide(15, 5))\n    fmt.Println(divide(4, 0))\n    fmt.Println(\"Program has been finished\")\n}\nfunc divide(x, y float64) float64{\n    if y == 0{ \n        panic(\"Division by zero!\")\n    }\n    return x / y\n}", "destination": "file", "file": "app.go", "env": "", "language": "go"}]}', '{"type": "Steps", "data": [{"type": "Run", "command": "go run app.go", "stdin": true, "stdout": true, "exitCode": true, "echo": true}]}');
INSERT INTO public.page VALUES (6, 'Каналы', 'Каналы', 'Каналы (channels) представляют инструменты коммуникации между горутинами. Для определения канала применяется ключевое слово chan:

После слова chan указывается тип данных, которые будут передаться с помощью канала. Например:

`var intCh chan int`

Если ранее в канал было отправлено число 5, то при выполнении операции <- intCh мы можем получить это число в переменную val.

Стоит учитывать, что мы можем отправить в канал и получить из канала данные только того типа, который представляет канал. Так, в примере с каналом intCh это данные типа int.

Как правило, отправителем данных является одна горутина, а получателем - другая горутина.

При простом определении переменной канала она имеет значение nil, то есть по сути канал неинициализирован. Для инициализации применяется функция make(). В зависимости от определения емкости канала он может быть буферизированным или небуферизированным.

## Небуфферизированные каналы

Для создания небуферизированного канала вызывается функция make() без указания емкости канала:

```
var intCh chan int = make(chan int) // канал для данных типа int
strCh := make(chan string)  // канал для данных типа string
```

Если канал пустой, то горутина-получатель блокируется, пока в канале не окажутся данные. Когда горутина-отправитель посылает данные, горутина-получатель получает эти данные и возобновляет работу.

Горутина-отправитель может отправлять данные только в пустой канал. Горутина-отправитель блокируется до тех пор, пока данные из канала не будут получены. Например:


', '1', 'golang:alpine', false, '{"data": [{"name": "123", "description": "", "type": "code", "values": [{"title": "title 1", "value": "1"}], "default": "package main\nimport \"fmt\"\n \nfunc main() {\n     \n    intCh := make(chan int) \n     \n    go func(){\n            fmt.Println(\"Go routine starts\")\n            intCh <- 5 // \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0430, \u043f\u043e\u043a\u0430 \u0434\u0430\u043d\u043d\u044b\u0435 \u043d\u0435 \u0431\u0443\u0434\u0443\u0442 \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u044b \u0444\u0443\u043d\u043a\u0446\u0438\u0435\u0439 main\n    }()\n    fmt.Println(<-intCh) // \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u0435 \u0434\u0430\u043d\u043d\u044b\u0445 \u0438\u0437 \u043a\u0430\u043d\u0430\u043b\u0430\n    fmt.Println(\"The End\")\n}", "destination": "file", "file": "app.go", "env": "", "language": "go"}]}', '{"type": "Steps", "data": [{"type": "Run", "command": "go run app.go", "stdin": true, "stdout": true, "exitCode": true, "echo": true}]}');
INSERT INTO public.page VALUES (7, 'WaitGroup', 'go_page_waitgroup', 'Еще одну возможность по синхронизации горутин представляет использование типа sync.WaitGroup. Этот тип позволяет определить группу горутин, которые должны выполняться вместе как одна группа. И можно установить блокировку, которая приостановит выполнение функции, пока не завершит выполнение вся группа горутин.

Вначале определяем группу в виде переменной wg sync.WaitGroup. С помощью метода Add определяем, что группа будет состоять из двух элементов

Все элементы группы wg будут представлять анонимную функцию в виде переменной work, которая в качестве параметра принимает условный числовой идентификатор горутины. Эта функция будет вызываться в виде горутин. Чтобы сигнализировать, что элемент группы завершил свое выполнение, в горутине необходимо вызвать метод Done()

Вызов метода wg.Done() уменьшает внутренний счетчик активных элементов на единицу.

В самой функции work() с помощью задержки времени на две секунды (time.Sleep(2 * time.Second)) имитируется работа горутины

Далее вызываем две горутины

Причем количество горутин, которые вызывают метод wg.Done() должно соответствовать количеству элементов группы wg, то есть в данном случае 2 элемента.

Затем вызывается метод Wait(), который ожидает завершения всех горутин из группы wg

Метод деблокирует функцию main, когда внутренний счетчик активных элементов в группе wg стает равен 0. Поэтому когда все горутины из группы wg завершат выполнение, функция main продолжит свою работу

', '1', 'golang:alpine', false, '{"data": [{"name": "123", "description": "", "type": "code", "values": [{"title": "title 1", "value": "1"}], "default": "package main\nimport (\n\"fmt\"\n\"sync\"\n\"time\"\n)\n  \n    \nfunc main() { \n    var wg sync.WaitGroup \n    wg.Add(2)       // \u0432 \u0433\u0440\u0443\u043f\u043f\u0435 \u0434\u0432\u0435 \u0433\u043e\u0440\u0443\u0442\u0438\u043d\u044b\n    work := func(id int) { \n        defer wg.Done()\n        fmt.Printf(\"\u0413\u043e\u0440\u0443\u0442\u0438\u043d\u0430 %d \u043d\u0430\u0447\u0430\u043b\u0430 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \\n\", id) \n        time.Sleep(2 * time.Second)\n        fmt.Printf(\"\u0413\u043e\u0440\u0443\u0442\u0438\u043d\u0430 %d \u0437\u0430\u0432\u0435\u0440\u0448\u0438\u043b\u0430 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \\n\", id) \n   } \n   \n   // \u0432\u044b\u0437\u044b\u0432\u0430\u0435\u043c \u0433\u043e\u0440\u0443\u0442\u0438\u043d\u044b\n   go work(1) \n   go work(2) \n   \n   wg.Wait()        // \u043e\u0436\u0438\u0434\u0430\u0435\u043c \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u044f \u043e\u0431\u043e\u0438\u0445 \u0433\u043e\u0440\u0443\u0442\u0438\u043d\n   fmt.Println(\"\u0413\u043e\u0440\u0443\u0442\u0438\u043d\u044b \u0437\u0430\u0432\u0435\u0440\u0448\u0438\u043b\u0438 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435\") \n}", "destination": "file", "file": "app.go", "env": "", "language": "go"}]}', '{"type": "Steps", "data": [{"type": "Run", "command": "go run app.go", "stdin": true, "stdout": true, "exitCode": true, "echo": true}]}');
INSERT INTO public.page VALUES (4, 'Горутины', 'Горутины', 'Горутины (goroutines) представляют параллельные операции, которые могут выполняться независимо от функции, в которой они запущены. Главная особенность горутин состоит в том, что они могут выполняться параллельно. То есть на многоядерных архитектурах есть возможность выполнять отдельные горутины на отдельных ядрах процессора, тем самым горутины будут выполняться паралелльно, и программа завершится быстрее.

Каждая горутина, как правило, представляет вызов функции, и последовательно выполняет все свои инструкции. Когда мы запускаем программу на Go, мы уже работаем как минимум с одной горутиной, которая представлена функцией main. Эта функция последовательно выполняет все инструкции, которые определены внутри нее.

Для определения горутин применяется оператор go, который ставится перед вызовом функции
', '1', 'golang:alpine', false, '{"data": [{"name": "123", "description": "", "type": "code", "values": [{"title": "title 1", "value": "1"}], "default": "package main\nimport \"fmt\"\n \nfunc main() {\n     \n    for i := 1; i < 7; i++{\n         \n        go func(n int){\n            result := 1\n            for j := 1; j <= n; j++{\n                result *= j\n            }\n            fmt.Println(n, \"-\", result)\n        }(i)\n    }\n    fmt.Scanln()\n    fmt.Println(\"The End\")\n}", "destination": "file", "file": "", "env": "", "language": "go"}]}', '{"type": "Steps", "data": [{"type": "Run", "command": "go run app.go", "stdin": true, "stdout": true, "exitCode": true, "echo": true}]}');
INSERT INTO public.page VALUES (8, 'Передача параметров', 'Передача параметров', 'UI описывает элементы ввода

- ввод текста
- чисел
- редактор кода с подсветкой синтаксиса
- файл(?)
', '', 'python:alpine', false, '{"data": [{"name": "param1", "description": "", "type": "code", "values": [], "default": "import os\n\n\nprint(os.environ)\n\nprint(open(''file.txt'').read())", "destination": "file", "file": "main.py", "env": "", "language": "python"}, {"name": "param2", "description": "", "type": "code", "values": [], "default": "hello", "destination": "file", "file": "file.txt", "env": "", "language": "python"}, {"name": "VARIABLE", "description": "", "type": "text", "values": [], "default": "123", "destination": "env", "file": "main.py", "env": "VARIABLE", "language": "python"}, {"name": "optimization", "description": "", "type": "list", "values": [{"title": "zero", "value": "-o0"}, {"title": "small", "value": "-o1"}, {"title": "all", "value": "-o2"}], "default": "-o0", "destination": "param", "file": "main.py", "env": "", "language": "python"}]}', '{"type": "Steps", "data": [{"type": "Run", "command": "echo gcc main.c $optimization", "stdin": true, "stdout": true, "exitCode": true, "echo": true}, {"type": "Run", "command": "python main.py", "stdin": true, "stdout": true, "exitCode": true, "echo": true}]}');


--
-- TOC entry 3349 (class 0 OID 16412)
-- Dependencies: 219
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public.project VALUES (4, 'Книга по языку GO', 'Интерактивное пособие для самых маленьких', true, '{"description": "", "data": [{"id": 1, "short_description": "\u041f\u0435\u0440\u0432\u0430\u044f \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430"}, {"id": 2, "short_description": "\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435"}, {"id": 3, "short_description": "defer \u0438 panic"}, {"description": "\u041f\u0440\u043e\u0434\u0432\u0438\u043d\u0443\u0442\u044b\u0435 \u0442\u0435\u043c\u044b", "data": [{"id": 4, "short_description": "\u0413\u043e\u0440\u0443\u0442\u0438\u043d\u044b"}, {"id": 6, "short_description": "\u041a\u0430\u043d\u0430\u043b\u044b"}, {"id": 7, "short_description": "WaitGroup"}]}]}');
INSERT INTO public.project VALUES (5, 'Демонстрация возможностей', 'Видно только администратору', false, '{"description": "", "data": [{"id": 8, "short_description": "\u041f\u0435\u0440\u0435\u0434\u0430\u0447\u0430 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432"}, {"description": "\u0420\u0430\u0437\u0434\u0435\u043b 1", "data": [{"id": 2, "short_description": "\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435"}, {"id": 1, "short_description": "\u041f\u0435\u0440\u0432\u0430\u044f \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430"}, {"id": 4, "short_description": "\u0413\u043e\u0440\u0443\u0442\u0438\u043d\u044b"}, {"description": "\u041f\u043e\u0434\u0440\u0430\u0437\u0434\u0435\u043b", "data": [{"id": 3, "short_description": "defer \u0438 panic"}, {"id": 4, "short_description": "\u0413\u043e\u0440\u0443\u0442\u0438\u043d\u044b"}]}, {"description": "\u0427\u0442\u043e-\u0442\u043e \u0435\u0449\u0435", "data": [{"id": 4, "short_description": "\u0413\u043e\u0440\u0443\u0442\u0438\u043d\u044b"}, {"id": 8, "short_description": "\u041f\u0435\u0440\u0435\u0434\u0430\u0447\u0430 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432"}]}, {"id": 2, "short_description": "\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435"}, {"description": "1", "data": [{"id": 7, "short_description": "go_page_waitgroup"}, {"id": 3, "short_description": "defer \u0438 panic"}, {"description": "2", "data": [{"id": 2, "short_description": "\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435"}, {"description": "3", "data": [{"id": 1, "short_description": "\u041f\u0435\u0440\u0432\u0430\u044f \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430"}, {"description": "4", "data": [{"id": 2, "short_description": "\u041f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435"}, {"id": 4, "short_description": "\u0413\u043e\u0440\u0443\u0442\u0438\u043d\u044b"}]}, {"id": 7, "short_description": "go_page_waitgroup"}]}]}, {"id": 3, "short_description": "defer \u0438 panic"}]}]}]}');


--
-- TOC entry 3347 (class 0 OID 16403)
-- Dependencies: 217
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: root
--

INSERT INTO public."user" VALUES (1, 'semwai', 'e14s@mail.ru', 'admin');
INSERT INTO public."user" VALUES (2, 'Semwai', 'vonderschah@gmail.com', 'user');


--
-- TOC entry 3358 (class 0 OID 0)
-- Dependencies: 214
-- Name: page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.page_id_seq', 8, true);


--
-- TOC entry 3359 (class 0 OID 0)
-- Dependencies: 218
-- Name: project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.project_id_seq', 5, true);


--
-- TOC entry 3360 (class 0 OID 0)
-- Dependencies: 216
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.user_id_seq', 2, true);


--
-- TOC entry 3195 (class 2606 OID 16399)
-- Name: page page_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.page
    ADD CONSTRAINT page_pkey PRIMARY KEY (id);


--
-- TOC entry 3197 (class 2606 OID 16401)
-- Name: page page_short_description_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.page
    ADD CONSTRAINT page_short_description_key UNIQUE (short_description);


--
-- TOC entry 3201 (class 2606 OID 16419)
-- Name: project project_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (id);


--
-- TOC entry 3199 (class 2606 OID 16410)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


-- Completed on 2023-05-11 22:02:20 UTC

--
-- PostgreSQL database dump complete
--

