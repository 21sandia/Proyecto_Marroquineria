PGDMP     )    3                {         
   EcommerceM    15.3    15.3 �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    35039 
   EcommerceM    DATABASE     �   CREATE DATABASE "EcommerceM" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Colombia.1252';
    DROP DATABASE "EcommerceM";
                postgres    false            �            1259    35040 
   cart_items    TABLE     �   CREATE TABLE public.cart_items (
    id integer NOT NULL,
    fk_id_product integer,
    fk_id_cart integer,
    quantity integer,
    total_price numeric(10,2)
);
    DROP TABLE public.cart_items;
       public         heap    postgres    false            �            1259    35043    cart_items_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cart_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.cart_items_id_seq;
       public          postgres    false    214            �           0    0    cart_items_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.cart_items_id_seq OWNED BY public.cart_items.id;
          public          postgres    false    215            �            1259    35044    carts    TABLE     �   CREATE TABLE public.carts (
    id integer NOT NULL,
    fk_id_user integer,
    created_ad timestamp without time zone,
    updated_ad timestamp without time zone
);
    DROP TABLE public.carts;
       public         heap    postgres    false            �            1259    35047    carts_id_seq    SEQUENCE     �   CREATE SEQUENCE public.carts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.carts_id_seq;
       public          postgres    false    216            �           0    0    carts_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.carts_id_seq OWNED BY public.carts.id;
          public          postgres    false    217            �            1259    35048 	   categorys    TABLE     [   CREATE TABLE public.categorys (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.categorys;
       public         heap    postgres    false            �            1259    35051    categorys_id_seq    SEQUENCE     �   CREATE SEQUENCE public.categorys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.categorys_id_seq;
       public          postgres    false    218            �           0    0    categorys_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.categorys_id_seq OWNED BY public.categorys.id;
          public          postgres    false    219            �            1259    35052    detail_prods    TABLE     &  CREATE TABLE public.detail_prods (
    id integer NOT NULL,
    fk_id_product integer,
    fk_id_measures integer,
    fk_id_materials integer,
    date date DEFAULT CURRENT_DATE NOT NULL,
    color character varying(30),
    size_p character varying(50),
    material character varying(40)
);
     DROP TABLE public.detail_prods;
       public         heap    postgres    false            �            1259    35056    detail_prods_id_seq    SEQUENCE     �   CREATE SEQUENCE public.detail_prods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.detail_prods_id_seq;
       public          postgres    false    220            �           0    0    detail_prods_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.detail_prods_id_seq OWNED BY public.detail_prods.id;
          public          postgres    false    221            �            1259    35057    detail_sales    TABLE     �   CREATE TABLE public.detail_sales (
    id integer NOT NULL,
    fk_id_sale integer,
    fk_id_prod integer,
    quantity integer,
    price_unit numeric(10,2),
    total_product numeric(10,2)
);
     DROP TABLE public.detail_sales;
       public         heap    postgres    false            �            1259    35060    detail_sales_id_seq    SEQUENCE     �   CREATE SEQUENCE public.detail_sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.detail_sales_id_seq;
       public          postgres    false    222            �           0    0    detail_sales_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.detail_sales_id_seq OWNED BY public.detail_sales.id;
          public          postgres    false    223            �            1259    35061 	   materials    TABLE     [   CREATE TABLE public.materials (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.materials;
       public         heap    postgres    false            �            1259    35064    materials_id_seq    SEQUENCE     �   CREATE SEQUENCE public.materials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.materials_id_seq;
       public          postgres    false    224            �           0    0    materials_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.materials_id_seq OWNED BY public.materials.id;
          public          postgres    false    225            �            1259    35065    measures    TABLE     Z   CREATE TABLE public.measures (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.measures;
       public         heap    postgres    false            �            1259    35068    measures_id_seq    SEQUENCE     �   CREATE SEQUENCE public.measures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.measures_id_seq;
       public          postgres    false    226            �           0    0    measures_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.measures_id_seq OWNED BY public.measures.id;
          public          postgres    false    227            �            1259    35240    order_items    TABLE     �   CREATE TABLE public.order_items (
    id integer NOT NULL,
    fk_id_order integer,
    product integer,
    quantity integer,
    price numeric(10,2),
    CONSTRAINT order_items_quantity_check CHECK ((quantity > 0))
);
    DROP TABLE public.order_items;
       public         heap    postgres    false            �            1259    35239    order_items_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.order_items_id_seq;
       public          postgres    false    245            �           0    0    order_items_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.order_items_id_seq OWNED BY public.order_items.id;
          public          postgres    false    244            �            1259    35223    orders    TABLE     �   CREATE TABLE public.orders (
    id integer NOT NULL,
    fk_id_state integer,
    fk_id_user integer,
    total_price numeric(10,2),
    address character varying(255),
    date timestamp with time zone
);
    DROP TABLE public.orders;
       public         heap    postgres    false            �            1259    35222    orders_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.orders_id_seq;
       public          postgres    false    243            �           0    0    orders_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;
          public          postgres    false    242            �            1259    35069    peoples    TABLE     �  CREATE TABLE public.peoples (
    id integer NOT NULL,
    email character varying(50),
    name character varying(30),
    last_name character varying(30),
    type_document character varying(30),
    document integer,
    gender character varying(30),
    date_birth date,
    phone character varying(10),
    address character varying(30),
    employee boolean,
    customer boolean,
    supplier boolean,
    is_guest boolean
);
    DROP TABLE public.peoples;
       public         heap    postgres    false            �            1259    35072    peoples_id_seq    SEQUENCE     �   CREATE SEQUENCE public.peoples_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.peoples_id_seq;
       public          postgres    false    228            �           0    0    peoples_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.peoples_id_seq OWNED BY public.peoples.id;
          public          postgres    false    229            �            1259    35073    products    TABLE     R  CREATE TABLE public.products (
    id integer NOT NULL,
    fk_id_state integer,
    fk_id_type_prod integer,
    name character varying(30),
    image character varying(500),
    reference character varying(60),
    description character varying(1000),
    quantity integer,
    price_shop numeric(10,2),
    price_sale numeric(10,2)
);
    DROP TABLE public.products;
       public         heap    postgres    false            �            1259    35078    products_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.products_id_seq;
       public          postgres    false    230            �           0    0    products_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;
          public          postgres    false    231            �            1259    35079    rol    TABLE     U   CREATE TABLE public.rol (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.rol;
       public         heap    postgres    false            �            1259    35082 
   rol_id_seq    SEQUENCE     �   CREATE SEQUENCE public.rol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.rol_id_seq;
       public          postgres    false    232            �           0    0 
   rol_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.rol_id_seq OWNED BY public.rol.id;
          public          postgres    false    233            �            1259    35083    sales    TABLE     �   CREATE TABLE public.sales (
    id integer NOT NULL,
    fk_id_state integer,
    fk_id_people integer,
    date date DEFAULT CURRENT_DATE NOT NULL,
    total_sale numeric(10,2)
);
    DROP TABLE public.sales;
       public         heap    postgres    false            �            1259    35087    sales_id_seq    SEQUENCE     �   CREATE SEQUENCE public.sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.sales_id_seq;
       public          postgres    false    234            �           0    0    sales_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.sales_id_seq OWNED BY public.sales.id;
          public          postgres    false    235            �            1259    35088    states    TABLE     X   CREATE TABLE public.states (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.states;
       public         heap    postgres    false            �            1259    35091    states_id_seq    SEQUENCE     �   CREATE SEQUENCE public.states_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.states_id_seq;
       public          postgres    false    236            �           0    0    states_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.states_id_seq OWNED BY public.states.id;
          public          postgres    false    237            �            1259    35092 
   type_prods    TABLE     x   CREATE TABLE public.type_prods (
    id integer NOT NULL,
    fk_id_category integer,
    name character varying(30)
);
    DROP TABLE public.type_prods;
       public         heap    postgres    false            �            1259    35095    type_prods_id_seq    SEQUENCE     �   CREATE SEQUENCE public.type_prods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.type_prods_id_seq;
       public          postgres    false    238            �           0    0    type_prods_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.type_prods_id_seq OWNED BY public.type_prods.id;
          public          postgres    false    239            �            1259    35096    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    fk_id_state integer,
    fk_id_rol integer,
    fk_id_people integer,
    password character varying(100),
    last_login timestamp without time zone
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    35099    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    240            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    241            �           2604    35100    cart_items id    DEFAULT     n   ALTER TABLE ONLY public.cart_items ALTER COLUMN id SET DEFAULT nextval('public.cart_items_id_seq'::regclass);
 <   ALTER TABLE public.cart_items ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214            �           2604    35101    carts id    DEFAULT     d   ALTER TABLE ONLY public.carts ALTER COLUMN id SET DEFAULT nextval('public.carts_id_seq'::regclass);
 7   ALTER TABLE public.carts ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216            �           2604    35102    categorys id    DEFAULT     l   ALTER TABLE ONLY public.categorys ALTER COLUMN id SET DEFAULT nextval('public.categorys_id_seq'::regclass);
 ;   ALTER TABLE public.categorys ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218            �           2604    35103    detail_prods id    DEFAULT     r   ALTER TABLE ONLY public.detail_prods ALTER COLUMN id SET DEFAULT nextval('public.detail_prods_id_seq'::regclass);
 >   ALTER TABLE public.detail_prods ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    220            �           2604    35104    detail_sales id    DEFAULT     r   ALTER TABLE ONLY public.detail_sales ALTER COLUMN id SET DEFAULT nextval('public.detail_sales_id_seq'::regclass);
 >   ALTER TABLE public.detail_sales ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    223    222            �           2604    35105    materials id    DEFAULT     l   ALTER TABLE ONLY public.materials ALTER COLUMN id SET DEFAULT nextval('public.materials_id_seq'::regclass);
 ;   ALTER TABLE public.materials ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    225    224            �           2604    35106    measures id    DEFAULT     j   ALTER TABLE ONLY public.measures ALTER COLUMN id SET DEFAULT nextval('public.measures_id_seq'::regclass);
 :   ALTER TABLE public.measures ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    227    226            �           2604    35243    order_items id    DEFAULT     p   ALTER TABLE ONLY public.order_items ALTER COLUMN id SET DEFAULT nextval('public.order_items_id_seq'::regclass);
 =   ALTER TABLE public.order_items ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    244    245    245            �           2604    35226 	   orders id    DEFAULT     f   ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);
 8   ALTER TABLE public.orders ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    243    242    243            �           2604    35107 
   peoples id    DEFAULT     h   ALTER TABLE ONLY public.peoples ALTER COLUMN id SET DEFAULT nextval('public.peoples_id_seq'::regclass);
 9   ALTER TABLE public.peoples ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    229    228            �           2604    35108    products id    DEFAULT     j   ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);
 :   ALTER TABLE public.products ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    231    230            �           2604    35109    rol id    DEFAULT     `   ALTER TABLE ONLY public.rol ALTER COLUMN id SET DEFAULT nextval('public.rol_id_seq'::regclass);
 5   ALTER TABLE public.rol ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    233    232            �           2604    35110    sales id    DEFAULT     d   ALTER TABLE ONLY public.sales ALTER COLUMN id SET DEFAULT nextval('public.sales_id_seq'::regclass);
 7   ALTER TABLE public.sales ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    235    234            �           2604    35111 	   states id    DEFAULT     f   ALTER TABLE ONLY public.states ALTER COLUMN id SET DEFAULT nextval('public.states_id_seq'::regclass);
 8   ALTER TABLE public.states ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    237    236            �           2604    35112    type_prods id    DEFAULT     n   ALTER TABLE ONLY public.type_prods ALTER COLUMN id SET DEFAULT nextval('public.type_prods_id_seq'::regclass);
 <   ALTER TABLE public.type_prods ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    239    238            �           2604    35113    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    241    240            �          0    35040 
   cart_items 
   TABLE DATA           Z   COPY public.cart_items (id, fk_id_product, fk_id_cart, quantity, total_price) FROM stdin;
    public          postgres    false    214   ԛ       �          0    35044    carts 
   TABLE DATA           G   COPY public.carts (id, fk_id_user, created_ad, updated_ad) FROM stdin;
    public          postgres    false    216   �       �          0    35048 	   categorys 
   TABLE DATA           -   COPY public.categorys (id, name) FROM stdin;
    public          postgres    false    218   m�       �          0    35052    detail_prods 
   TABLE DATA           y   COPY public.detail_prods (id, fk_id_product, fk_id_measures, fk_id_materials, date, color, size_p, material) FROM stdin;
    public          postgres    false    220   ��       �          0    35057    detail_sales 
   TABLE DATA           g   COPY public.detail_sales (id, fk_id_sale, fk_id_prod, quantity, price_unit, total_product) FROM stdin;
    public          postgres    false    222   D�       �          0    35061 	   materials 
   TABLE DATA           -   COPY public.materials (id, name) FROM stdin;
    public          postgres    false    224   3�       �          0    35065    measures 
   TABLE DATA           ,   COPY public.measures (id, name) FROM stdin;
    public          postgres    false    226   m�       �          0    35240    order_items 
   TABLE DATA           P   COPY public.order_items (id, fk_id_order, product, quantity, price) FROM stdin;
    public          postgres    false    245   Þ       �          0    35223    orders 
   TABLE DATA           Y   COPY public.orders (id, fk_id_state, fk_id_user, total_price, address, date) FROM stdin;
    public          postgres    false    243   ��       �          0    35069    peoples 
   TABLE DATA           �   COPY public.peoples (id, email, name, last_name, type_document, document, gender, date_birth, phone, address, employee, customer, supplier, is_guest) FROM stdin;
    public          postgres    false    228   ��       �          0    35073    products 
   TABLE DATA           �   COPY public.products (id, fk_id_state, fk_id_type_prod, name, image, reference, description, quantity, price_shop, price_sale) FROM stdin;
    public          postgres    false    230   +�       �          0    35079    rol 
   TABLE DATA           '   COPY public.rol (id, name) FROM stdin;
    public          postgres    false    232   n�       �          0    35083    sales 
   TABLE DATA           P   COPY public.sales (id, fk_id_state, fk_id_people, date, total_sale) FROM stdin;
    public          postgres    false    234   ��       �          0    35088    states 
   TABLE DATA           *   COPY public.states (id, name) FROM stdin;
    public          postgres    false    236   4�       �          0    35092 
   type_prods 
   TABLE DATA           >   COPY public.type_prods (id, fk_id_category, name) FROM stdin;
    public          postgres    false    238   ��       �          0    35096    users 
   TABLE DATA           _   COPY public.users (id, fk_id_state, fk_id_rol, fk_id_people, password, last_login) FROM stdin;
    public          postgres    false    240   �       �           0    0    cart_items_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.cart_items_id_seq', 18, true);
          public          postgres    false    215            �           0    0    carts_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.carts_id_seq', 3, true);
          public          postgres    false    217            �           0    0    categorys_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.categorys_id_seq', 5, true);
          public          postgres    false    219            �           0    0    detail_prods_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.detail_prods_id_seq', 8, true);
          public          postgres    false    221            �           0    0    detail_sales_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.detail_sales_id_seq', 108, true);
          public          postgres    false    223            �           0    0    materials_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.materials_id_seq', 2, true);
          public          postgres    false    225            �           0    0    measures_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.measures_id_seq', 8, true);
          public          postgres    false    227            �           0    0    order_items_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.order_items_id_seq', 1, false);
          public          postgres    false    244            �           0    0    orders_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.orders_id_seq', 6, true);
          public          postgres    false    242            �           0    0    peoples_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.peoples_id_seq', 34, true);
          public          postgres    false    229            �           0    0    products_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.products_id_seq', 12, true);
          public          postgres    false    231            �           0    0 
   rol_id_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('public.rol_id_seq', 6, true);
          public          postgres    false    233            �           0    0    sales_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.sales_id_seq', 62, true);
          public          postgres    false    235            �           0    0    states_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.states_id_seq', 5, true);
          public          postgres    false    237            �           0    0    type_prods_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.type_prods_id_seq', 8, true);
          public          postgres    false    239            �           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 17, true);
          public          postgres    false    241            �           2606    35115    cart_items cart_items_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.cart_items DROP CONSTRAINT cart_items_pkey;
       public            postgres    false    214            �           2606    35117    carts carts_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.carts DROP CONSTRAINT carts_pkey;
       public            postgres    false    216            �           2606    35119    categorys categorys_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.categorys
    ADD CONSTRAINT categorys_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.categorys DROP CONSTRAINT categorys_pkey;
       public            postgres    false    218            �           2606    35121    detail_prods detail_prods_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_pkey;
       public            postgres    false    220            �           2606    35123    detail_sales detail_sales_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.detail_sales
    ADD CONSTRAINT detail_sales_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.detail_sales DROP CONSTRAINT detail_sales_pkey;
       public            postgres    false    222            �           2606    35125    materials materials_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.materials DROP CONSTRAINT materials_pkey;
       public            postgres    false    224            �           2606    35127    measures measures_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.measures
    ADD CONSTRAINT measures_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.measures DROP CONSTRAINT measures_pkey;
       public            postgres    false    226            �           2606    35246    order_items order_items_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_pkey;
       public            postgres    false    245            �           2606    35228    orders orders_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public            postgres    false    243            �           2606    35129    peoples peoples_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.peoples
    ADD CONSTRAINT peoples_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.peoples DROP CONSTRAINT peoples_pkey;
       public            postgres    false    228            �           2606    35131    products products_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public            postgres    false    230            �           2606    35133    rol rol_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id);
 6   ALTER TABLE ONLY public.rol DROP CONSTRAINT rol_pkey;
       public            postgres    false    232            �           2606    35135    sales sales_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_pkey;
       public            postgres    false    234            �           2606    35137    states states_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.states
    ADD CONSTRAINT states_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.states DROP CONSTRAINT states_pkey;
       public            postgres    false    236            �           2606    35139    type_prods type_prods_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.type_prods
    ADD CONSTRAINT type_prods_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.type_prods DROP CONSTRAINT type_prods_pkey;
       public            postgres    false    238            �           2606    35141    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    240            �           2606    35142 %   cart_items cart_items_fk_id_cart_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_fk_id_cart_fkey FOREIGN KEY (fk_id_cart) REFERENCES public.carts(id);
 O   ALTER TABLE ONLY public.cart_items DROP CONSTRAINT cart_items_fk_id_cart_fkey;
       public          postgres    false    3270    216    214            �           2606    35147 (   cart_items cart_items_fk_id_product_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_fk_id_product_fkey FOREIGN KEY (fk_id_product) REFERENCES public.products(id);
 R   ALTER TABLE ONLY public.cart_items DROP CONSTRAINT cart_items_fk_id_product_fkey;
       public          postgres    false    214    3284    230            �           2606    35152    carts carts_fk_id_user_fkey    FK CONSTRAINT     }   ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_fk_id_user_fkey FOREIGN KEY (fk_id_user) REFERENCES public.users(id);
 E   ALTER TABLE ONLY public.carts DROP CONSTRAINT carts_fk_id_user_fkey;
       public          postgres    false    3294    240    216            �           2606    35157 .   detail_prods detail_prods_fk_id_materials_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_fk_id_materials_fkey FOREIGN KEY (fk_id_materials) REFERENCES public.materials(id);
 X   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_fk_id_materials_fkey;
       public          postgres    false    224    3278    220            �           2606    35162 -   detail_prods detail_prods_fk_id_measures_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_fk_id_measures_fkey FOREIGN KEY (fk_id_measures) REFERENCES public.measures(id);
 W   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_fk_id_measures_fkey;
       public          postgres    false    220    226    3280            �           2606    35167 ,   detail_prods detail_prods_fk_id_product_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_fk_id_product_fkey FOREIGN KEY (fk_id_product) REFERENCES public.products(id);
 V   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_fk_id_product_fkey;
       public          postgres    false    220    3284    230            �           2606    35172 )   detail_sales detail_sales_fk_id_prod_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_sales
    ADD CONSTRAINT detail_sales_fk_id_prod_fkey FOREIGN KEY (fk_id_prod) REFERENCES public.products(id);
 S   ALTER TABLE ONLY public.detail_sales DROP CONSTRAINT detail_sales_fk_id_prod_fkey;
       public          postgres    false    3284    230    222            �           2606    35177 )   detail_sales detail_sales_fk_id_sale_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_sales
    ADD CONSTRAINT detail_sales_fk_id_sale_fkey FOREIGN KEY (fk_id_sale) REFERENCES public.sales(id);
 S   ALTER TABLE ONLY public.detail_sales DROP CONSTRAINT detail_sales_fk_id_sale_fkey;
       public          postgres    false    222    234    3288            �           2606    35247 (   order_items order_items_fk_id_order_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_fk_id_order_fkey FOREIGN KEY (fk_id_order) REFERENCES public.orders(id) ON DELETE CASCADE;
 R   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_fk_id_order_fkey;
       public          postgres    false    243    245    3296            �           2606    35252 $   order_items order_items_product_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_fkey FOREIGN KEY (product) REFERENCES public.products(id) ON DELETE CASCADE;
 N   ALTER TABLE ONLY public.order_items DROP CONSTRAINT order_items_product_fkey;
       public          postgres    false    245    230    3284            �           2606    35229    orders orders_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 H   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_fk_id_state_fkey;
       public          postgres    false    243    236    3290            �           2606    35234    orders orders_fk_id_user_fkey    FK CONSTRAINT        ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_fk_id_user_fkey FOREIGN KEY (fk_id_user) REFERENCES public.users(id);
 G   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_fk_id_user_fkey;
       public          postgres    false    240    243    3294            �           2606    35182 "   products products_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 L   ALTER TABLE ONLY public.products DROP CONSTRAINT products_fk_id_state_fkey;
       public          postgres    false    230    236    3290            �           2606    35187 &   products products_fk_id_type_prod_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_fk_id_type_prod_fkey FOREIGN KEY (fk_id_type_prod) REFERENCES public.type_prods(id);
 P   ALTER TABLE ONLY public.products DROP CONSTRAINT products_fk_id_type_prod_fkey;
       public          postgres    false    238    230    3292            �           2606    35192    sales sales_fk_id_people_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_fk_id_people_fkey FOREIGN KEY (fk_id_people) REFERENCES public.peoples(id);
 G   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_fk_id_people_fkey;
       public          postgres    false    234    228    3282            �           2606    35197    sales sales_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 F   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_fk_id_state_fkey;
       public          postgres    false    3290    236    234            �           2606    35202 )   type_prods type_prods_fk_id_category_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.type_prods
    ADD CONSTRAINT type_prods_fk_id_category_fkey FOREIGN KEY (fk_id_category) REFERENCES public.categorys(id);
 S   ALTER TABLE ONLY public.type_prods DROP CONSTRAINT type_prods_fk_id_category_fkey;
       public          postgres    false    3272    238    218            �           2606    35207    users users_fk_id_people_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_fk_id_people_fkey FOREIGN KEY (fk_id_people) REFERENCES public.peoples(id);
 G   ALTER TABLE ONLY public.users DROP CONSTRAINT users_fk_id_people_fkey;
       public          postgres    false    3282    228    240            �           2606    35212    users users_fk_id_rol_fkey    FK CONSTRAINT     y   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_fk_id_rol_fkey FOREIGN KEY (fk_id_rol) REFERENCES public.rol(id);
 D   ALTER TABLE ONLY public.users DROP CONSTRAINT users_fk_id_rol_fkey;
       public          postgres    false    3286    232    240            �           2606    35217    users users_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 F   ALTER TABLE ONLY public.users DROP CONSTRAINT users_fk_id_state_fkey;
       public          postgres    false    3290    236    240            �   $   x�3��4Bc3=.#NK� ���qqq dQK      �   U   x�u��� ��Ta:
Ԓ���3���]4xӥ+رK��T���P�a�>ʲ��t\*Ҏ��|�VD�s�g�*BM�)"/�!�      �   C   x�3�t��-(-IL�/J-�2���OO,�2��*MM/M-I-�L�2�J,H,�/�2��/H����� <�      �   t   x�}ϱ
� ����]�Բ����%PZ�@h��3(І�ߟ�`� �b-U/��p��G0�m�NqM��ݍ%�1������.٢�X�%��[���uЁ�7p ��������.�4�      �   �   x�m����0��J1ɖe�������p�𕀢V�<�6l��m}�����}���N~���,��[�[�c9��.��wX&�C��w����߽E~���n�[����o�}�R���O[ԷS�e��v���mQ�nq��-�{\�ퟰE}��'���{��)q��^�{Z������]8�.���Cz1��qx�@/�U/�Ŷ��������<��g��      �   *   x�3�t�I�O���2�tLN-�W��˯�LIL�I����� ��	�      �   F   x�3��2��2���2���2���2�4M�U�R04PH��2�44�q�rs�,8���\�l� ��      �      x������ � �      �   �   x���=
1@�:9E.���f�����&���(��Gwӈ�z����f��XҦ�/i��,։1�5�F�%�Oh�$���<��z�NUP)�8���8	W[���$C6�5d�H~S�>�?sS�"B���9uތ"��c1�'O�E�      �   �  x���Kr�0���)� ��G�w�vXtJ햍�c�I��0�\=B/V%�B�E�([�>��=�mY�%�ɡ�f��(-2���|U�}�C�Vu @ԱTRY3����H!�P�P(PBjcl�x�KS���P���X�F��7��Ug^�P�+R*�*�"�|\�3N��W�S��3��1�h�VQ%�B��
{h�ъ�g��C����jJ-Xl|�V7H��j�{ήh���#���#L`Yҁ��x���uPs/���vi�,ytV�F��G
�]H�1�eO(��%oa�$c��Q�lj� <�Dí�^^��"%:F���V�E�x�؞�b|}W�wqz�]�-�`��t��/6�������'� /E����J�3��U�TI�y��_�[�F�|�Cu>����~��(��O��      �   3  x�u��J�0�O�'�M�n�O��&� B9��2�K�!���������b�A8>\�!J���2nс�L����[�M�z�����oP��c�+&X�&y~<��hlY��Q�(�&�k�6���w7Ѣ����֊��_z�Y�|ۛ"x@�H��HVpDW\z��;�L���V��Q �Â˨�r�n&�A�3��BJ��f�*_{��b
'P�WMx_�B%�1$�O�֨״-	5��H=��^q�c/$�c�
�]�\n���N��-�|�z䯻�[�0:����=2�v5&�mQu����O���<˲�f�s      �   :   x�3�tL����,.)JL�/�2�t�-�I���9���RSA�&��9��y%�\1z\\\ �n�      �   l   x�}ѻ� E����������H��I��⺙�wOXd�Y�6��isbq����㸖�d#b��Cl�wI�$H�. ]@��t��k���y$�ԎWZUU?n�y�      �   =   x�3�tL.�,��2���K�0M8]2���2�rR�9�Rs2�S�L9��Rr1z\\\ ��F      �   v   x�U�11k�~"�qP#h%��D
9��'���pAC7��4бh�>���M99�PгM�+��/�k����^S�sW)xZ��mq��Mn���$y����3���`�/�%�      �   %  x�u�[o�P�g�N��=�����EA�,�i2��Њ�_?N;I��9g�YY�u^fO��}�¿�M���@�'��+�N��6��J����6�04��NW�Y6�G�� F���_(f?�{o�T��g#LC��AG\gj� X���~��xmͲ���dj�|}�RK9ˊ�]�`@��FI��2�Î��ڵv�$,6J�y����t�=�b���j��':�Ů@���6���(�H"+����d�}T���"
�-��X���h�0�.k���(��sS�N)����n���">�n�}f~[˘)8��6�n<'��5��޲h�W�j~zzZ���w]ө�)�V��%��v��CL�!�L��u��e�:��|��i�8^���r1G}M��i1��I�C�c�̠�4����G�L}s��\��-%[[c�PռF3q<��ě�.~h<g�6���/�Q���|�����f�	ٜm6���cD��cPʊ[��}��#3��o�t���U;��`yP��m�h��8���	�qP��y�I����މ     