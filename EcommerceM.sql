PGDMP                         {         
   EcommerceM    15.3    15.3 v    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    34388 
   EcommerceM    DATABASE     �   CREATE DATABASE "EcommerceM" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Colombia.1252';
    DROP DATABASE "EcommerceM";
                postgres    false            �            1259    34559 
   cart_items    TABLE     �   CREATE TABLE public.cart_items (
    id integer NOT NULL,
    fk_id_product integer,
    fk_id_cart integer,
    quantity integer,
    total_price numeric(10,2)
);
    DROP TABLE public.cart_items;
       public         heap    postgres    false            �            1259    34558    cart_items_id_seq    SEQUENCE     �   CREATE SEQUENCE public.cart_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.cart_items_id_seq;
       public          postgres    false    241            �           0    0    cart_items_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.cart_items_id_seq OWNED BY public.cart_items.id;
          public          postgres    false    240            �            1259    34547    carts    TABLE     �   CREATE TABLE public.carts (
    id integer NOT NULL,
    fk_id_user integer,
    created_ad timestamp without time zone,
    updated_ad timestamp without time zone
);
    DROP TABLE public.carts;
       public         heap    postgres    false            �            1259    34546    carts_id_seq    SEQUENCE     �   CREATE SEQUENCE public.carts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.carts_id_seq;
       public          postgres    false    239            �           0    0    carts_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.carts_id_seq OWNED BY public.carts.id;
          public          postgres    false    238            �            1259    34433 	   categorys    TABLE     [   CREATE TABLE public.categorys (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.categorys;
       public         heap    postgres    false            �            1259    34432    categorys_id_seq    SEQUENCE     �   CREATE SEQUENCE public.categorys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.categorys_id_seq;
       public          postgres    false    223            �           0    0    categorys_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.categorys_id_seq OWNED BY public.categorys.id;
          public          postgres    false    222            �            1259    34485    detail_prods    TABLE     &  CREATE TABLE public.detail_prods (
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
       public         heap    postgres    false            �            1259    34484    detail_prods_id_seq    SEQUENCE     �   CREATE SEQUENCE public.detail_prods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.detail_prods_id_seq;
       public          postgres    false    233            �           0    0    detail_prods_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.detail_prods_id_seq OWNED BY public.detail_prods.id;
          public          postgres    false    232            �            1259    34526    detail_sales    TABLE     �   CREATE TABLE public.detail_sales (
    id integer NOT NULL,
    fk_id_sale integer,
    fk_id_prod integer,
    quantity integer,
    price_unit numeric(10,2),
    total_product numeric(10,2)
);
     DROP TABLE public.detail_sales;
       public         heap    postgres    false            �            1259    34525    detail_sales_id_seq    SEQUENCE     �   CREATE SEQUENCE public.detail_sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.detail_sales_id_seq;
       public          postgres    false    237            �           0    0    detail_sales_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.detail_sales_id_seq OWNED BY public.detail_sales.id;
          public          postgres    false    236            �            1259    34478 	   materials    TABLE     [   CREATE TABLE public.materials (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.materials;
       public         heap    postgres    false            �            1259    34477    materials_id_seq    SEQUENCE     �   CREATE SEQUENCE public.materials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.materials_id_seq;
       public          postgres    false    231            �           0    0    materials_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.materials_id_seq OWNED BY public.materials.id;
          public          postgres    false    230            �            1259    34471    measures    TABLE     Z   CREATE TABLE public.measures (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.measures;
       public         heap    postgres    false            �            1259    34470    measures_id_seq    SEQUENCE     �   CREATE SEQUENCE public.measures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.measures_id_seq;
       public          postgres    false    229            �           0    0    measures_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.measures_id_seq OWNED BY public.measures.id;
          public          postgres    false    228            �            1259    34404    peoples    TABLE     �  CREATE TABLE public.peoples (
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
    empleado boolean,
    cliente boolean,
    proveedor boolean
);
    DROP TABLE public.peoples;
       public         heap    postgres    false            �            1259    34403    peoples_id_seq    SEQUENCE     �   CREATE SEQUENCE public.peoples_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.peoples_id_seq;
       public          postgres    false    219            �           0    0    peoples_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.peoples_id_seq OWNED BY public.peoples.id;
          public          postgres    false    218            �            1259    34452    products    TABLE     R  CREATE TABLE public.products (
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
       public         heap    postgres    false            �            1259    34451    products_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.products_id_seq;
       public          postgres    false    227            �           0    0    products_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;
          public          postgres    false    226            �            1259    34390    rol    TABLE     U   CREATE TABLE public.rol (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.rol;
       public         heap    postgres    false            �            1259    34389 
   rol_id_seq    SEQUENCE     �   CREATE SEQUENCE public.rol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.rol_id_seq;
       public          postgres    false    215            �           0    0 
   rol_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.rol_id_seq OWNED BY public.rol.id;
          public          postgres    false    214            �            1259    34508    sales    TABLE     �   CREATE TABLE public.sales (
    id integer NOT NULL,
    fk_id_state integer,
    fk_id_people integer,
    date date DEFAULT CURRENT_DATE NOT NULL,
    total_sale numeric(10,2)
);
    DROP TABLE public.sales;
       public         heap    postgres    false            �            1259    34507    sales_id_seq    SEQUENCE     �   CREATE SEQUENCE public.sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.sales_id_seq;
       public          postgres    false    235            �           0    0    sales_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.sales_id_seq OWNED BY public.sales.id;
          public          postgres    false    234            �            1259    34397    states    TABLE     X   CREATE TABLE public.states (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.states;
       public         heap    postgres    false            �            1259    34396    states_id_seq    SEQUENCE     �   CREATE SEQUENCE public.states_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.states_id_seq;
       public          postgres    false    217            �           0    0    states_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.states_id_seq OWNED BY public.states.id;
          public          postgres    false    216            �            1259    34440 
   type_prods    TABLE     x   CREATE TABLE public.type_prods (
    id integer NOT NULL,
    fk_id_category integer,
    name character varying(30)
);
    DROP TABLE public.type_prods;
       public         heap    postgres    false            �            1259    34439    type_prods_id_seq    SEQUENCE     �   CREATE SEQUENCE public.type_prods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.type_prods_id_seq;
       public          postgres    false    225            �           0    0    type_prods_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.type_prods_id_seq OWNED BY public.type_prods.id;
          public          postgres    false    224            �            1259    34411    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    fk_id_state integer,
    fk_id_rol integer,
    fk_id_people integer,
    password character varying(100),
    last_login timestamp without time zone
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    34410    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    221            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    220            �           2604    34562    cart_items id    DEFAULT     n   ALTER TABLE ONLY public.cart_items ALTER COLUMN id SET DEFAULT nextval('public.cart_items_id_seq'::regclass);
 <   ALTER TABLE public.cart_items ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    241    240    241            �           2604    34550    carts id    DEFAULT     d   ALTER TABLE ONLY public.carts ALTER COLUMN id SET DEFAULT nextval('public.carts_id_seq'::regclass);
 7   ALTER TABLE public.carts ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    239    238    239            �           2604    34436    categorys id    DEFAULT     l   ALTER TABLE ONLY public.categorys ALTER COLUMN id SET DEFAULT nextval('public.categorys_id_seq'::regclass);
 ;   ALTER TABLE public.categorys ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    223    223            �           2604    34488    detail_prods id    DEFAULT     r   ALTER TABLE ONLY public.detail_prods ALTER COLUMN id SET DEFAULT nextval('public.detail_prods_id_seq'::regclass);
 >   ALTER TABLE public.detail_prods ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    233    233            �           2604    34529    detail_sales id    DEFAULT     r   ALTER TABLE ONLY public.detail_sales ALTER COLUMN id SET DEFAULT nextval('public.detail_sales_id_seq'::regclass);
 >   ALTER TABLE public.detail_sales ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    237    236    237            �           2604    34481    materials id    DEFAULT     l   ALTER TABLE ONLY public.materials ALTER COLUMN id SET DEFAULT nextval('public.materials_id_seq'::regclass);
 ;   ALTER TABLE public.materials ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    231    231            �           2604    34474    measures id    DEFAULT     j   ALTER TABLE ONLY public.measures ALTER COLUMN id SET DEFAULT nextval('public.measures_id_seq'::regclass);
 :   ALTER TABLE public.measures ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    228    229    229            �           2604    34407 
   peoples id    DEFAULT     h   ALTER TABLE ONLY public.peoples ALTER COLUMN id SET DEFAULT nextval('public.peoples_id_seq'::regclass);
 9   ALTER TABLE public.peoples ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218    219            �           2604    34455    products id    DEFAULT     j   ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);
 :   ALTER TABLE public.products ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    227    226    227            �           2604    34393    rol id    DEFAULT     `   ALTER TABLE ONLY public.rol ALTER COLUMN id SET DEFAULT nextval('public.rol_id_seq'::regclass);
 5   ALTER TABLE public.rol ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214    215            �           2604    34511    sales id    DEFAULT     d   ALTER TABLE ONLY public.sales ALTER COLUMN id SET DEFAULT nextval('public.sales_id_seq'::regclass);
 7   ALTER TABLE public.sales ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    235    234    235            �           2604    34400 	   states id    DEFAULT     f   ALTER TABLE ONLY public.states ALTER COLUMN id SET DEFAULT nextval('public.states_id_seq'::regclass);
 8   ALTER TABLE public.states ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216    217            �           2604    34443    type_prods id    DEFAULT     n   ALTER TABLE ONLY public.type_prods ALTER COLUMN id SET DEFAULT nextval('public.type_prods_id_seq'::regclass);
 <   ALTER TABLE public.type_prods ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    225    224    225            �           2604    34414    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    221    221            �          0    34559 
   cart_items 
   TABLE DATA           Z   COPY public.cart_items (id, fk_id_product, fk_id_cart, quantity, total_price) FROM stdin;
    public          postgres    false    241   J�       �          0    34547    carts 
   TABLE DATA           G   COPY public.carts (id, fk_id_user, created_ad, updated_ad) FROM stdin;
    public          postgres    false    239   g�       y          0    34433 	   categorys 
   TABLE DATA           -   COPY public.categorys (id, name) FROM stdin;
    public          postgres    false    223   ��       �          0    34485    detail_prods 
   TABLE DATA           y   COPY public.detail_prods (id, fk_id_product, fk_id_measures, fk_id_materials, date, color, size_p, material) FROM stdin;
    public          postgres    false    233   ֆ       �          0    34526    detail_sales 
   TABLE DATA           g   COPY public.detail_sales (id, fk_id_sale, fk_id_prod, quantity, price_unit, total_product) FROM stdin;
    public          postgres    false    237   @�       �          0    34478 	   materials 
   TABLE DATA           -   COPY public.materials (id, name) FROM stdin;
    public          postgres    false    231   �                 0    34471    measures 
   TABLE DATA           ,   COPY public.measures (id, name) FROM stdin;
    public          postgres    false    229   �       u          0    34404    peoples 
   TABLE DATA           �   COPY public.peoples (id, email, name, last_name, type_document, document, gender, date_birth, phone, address, empleado, cliente, proveedor) FROM stdin;
    public          postgres    false    219   r�       }          0    34452    products 
   TABLE DATA           �   COPY public.products (id, fk_id_state, fk_id_type_prod, name, image, reference, description, quantity, price_shop, price_sale) FROM stdin;
    public          postgres    false    227   :�       q          0    34390    rol 
   TABLE DATA           '   COPY public.rol (id, name) FROM stdin;
    public          postgres    false    215   �       �          0    34508    sales 
   TABLE DATA           P   COPY public.sales (id, fk_id_state, fk_id_people, date, total_sale) FROM stdin;
    public          postgres    false    235   M�       s          0    34397    states 
   TABLE DATA           *   COPY public.states (id, name) FROM stdin;
    public          postgres    false    217   ��       {          0    34440 
   type_prods 
   TABLE DATA           >   COPY public.type_prods (id, fk_id_category, name) FROM stdin;
    public          postgres    false    225   ��       w          0    34411    users 
   TABLE DATA           _   COPY public.users (id, fk_id_state, fk_id_rol, fk_id_people, password, last_login) FROM stdin;
    public          postgres    false    221   ~�       �           0    0    cart_items_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.cart_items_id_seq', 1, false);
          public          postgres    false    240            �           0    0    carts_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.carts_id_seq', 1, false);
          public          postgres    false    238            �           0    0    categorys_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.categorys_id_seq', 5, true);
          public          postgres    false    222            �           0    0    detail_prods_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.detail_prods_id_seq', 5, true);
          public          postgres    false    232            �           0    0    detail_sales_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.detail_sales_id_seq', 26, true);
          public          postgres    false    236            �           0    0    materials_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.materials_id_seq', 2, true);
          public          postgres    false    230            �           0    0    measures_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.measures_id_seq', 8, true);
          public          postgres    false    228            �           0    0    peoples_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.peoples_id_seq', 8, true);
          public          postgres    false    218            �           0    0    products_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.products_id_seq', 9, true);
          public          postgres    false    226            �           0    0 
   rol_id_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('public.rol_id_seq', 4, true);
          public          postgres    false    214            �           0    0    sales_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.sales_id_seq', 21, true);
          public          postgres    false    234            �           0    0    states_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.states_id_seq', 5, true);
          public          postgres    false    216            �           0    0    type_prods_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.type_prods_id_seq', 8, true);
          public          postgres    false    224            �           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 5, true);
          public          postgres    false    220            �           2606    34564    cart_items cart_items_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.cart_items DROP CONSTRAINT cart_items_pkey;
       public            postgres    false    241            �           2606    34552    carts carts_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.carts DROP CONSTRAINT carts_pkey;
       public            postgres    false    239            �           2606    34438    categorys categorys_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.categorys
    ADD CONSTRAINT categorys_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.categorys DROP CONSTRAINT categorys_pkey;
       public            postgres    false    223            �           2606    34491    detail_prods detail_prods_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_pkey;
       public            postgres    false    233            �           2606    34531    detail_sales detail_sales_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.detail_sales
    ADD CONSTRAINT detail_sales_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.detail_sales DROP CONSTRAINT detail_sales_pkey;
       public            postgres    false    237            �           2606    34483    materials materials_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.materials DROP CONSTRAINT materials_pkey;
       public            postgres    false    231            �           2606    34476    measures measures_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.measures
    ADD CONSTRAINT measures_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.measures DROP CONSTRAINT measures_pkey;
       public            postgres    false    229            �           2606    34409    peoples peoples_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.peoples
    ADD CONSTRAINT peoples_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.peoples DROP CONSTRAINT peoples_pkey;
       public            postgres    false    219            �           2606    34459    products products_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public            postgres    false    227            �           2606    34395    rol rol_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id);
 6   ALTER TABLE ONLY public.rol DROP CONSTRAINT rol_pkey;
       public            postgres    false    215            �           2606    34514    sales sales_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_pkey;
       public            postgres    false    235            �           2606    34402    states states_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.states
    ADD CONSTRAINT states_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.states DROP CONSTRAINT states_pkey;
       public            postgres    false    217            �           2606    34445    type_prods type_prods_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.type_prods
    ADD CONSTRAINT type_prods_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.type_prods DROP CONSTRAINT type_prods_pkey;
       public            postgres    false    225            �           2606    34416    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    221            �           2606    34570 %   cart_items cart_items_fk_id_cart_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_fk_id_cart_fkey FOREIGN KEY (fk_id_cart) REFERENCES public.carts(id);
 O   ALTER TABLE ONLY public.cart_items DROP CONSTRAINT cart_items_fk_id_cart_fkey;
       public          postgres    false    239    241    3279            �           2606    34565 (   cart_items cart_items_fk_id_product_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_fk_id_product_fkey FOREIGN KEY (fk_id_product) REFERENCES public.products(id);
 R   ALTER TABLE ONLY public.cart_items DROP CONSTRAINT cart_items_fk_id_product_fkey;
       public          postgres    false    3267    227    241            �           2606    34553    carts carts_fk_id_user_fkey    FK CONSTRAINT     }   ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_fk_id_user_fkey FOREIGN KEY (fk_id_user) REFERENCES public.users(id);
 E   ALTER TABLE ONLY public.carts DROP CONSTRAINT carts_fk_id_user_fkey;
       public          postgres    false    239    221    3261            �           2606    34502 .   detail_prods detail_prods_fk_id_materials_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_fk_id_materials_fkey FOREIGN KEY (fk_id_materials) REFERENCES public.materials(id);
 X   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_fk_id_materials_fkey;
       public          postgres    false    3271    231    233            �           2606    34497 -   detail_prods detail_prods_fk_id_measures_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_fk_id_measures_fkey FOREIGN KEY (fk_id_measures) REFERENCES public.measures(id);
 W   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_fk_id_measures_fkey;
       public          postgres    false    233    229    3269            �           2606    34492 ,   detail_prods detail_prods_fk_id_product_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_fk_id_product_fkey FOREIGN KEY (fk_id_product) REFERENCES public.products(id);
 V   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_fk_id_product_fkey;
       public          postgres    false    227    3267    233            �           2606    34537 )   detail_sales detail_sales_fk_id_prod_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_sales
    ADD CONSTRAINT detail_sales_fk_id_prod_fkey FOREIGN KEY (fk_id_prod) REFERENCES public.products(id);
 S   ALTER TABLE ONLY public.detail_sales DROP CONSTRAINT detail_sales_fk_id_prod_fkey;
       public          postgres    false    237    227    3267            �           2606    34532 )   detail_sales detail_sales_fk_id_sale_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_sales
    ADD CONSTRAINT detail_sales_fk_id_sale_fkey FOREIGN KEY (fk_id_sale) REFERENCES public.sales(id);
 S   ALTER TABLE ONLY public.detail_sales DROP CONSTRAINT detail_sales_fk_id_sale_fkey;
       public          postgres    false    237    3275    235            �           2606    34460 "   products products_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 L   ALTER TABLE ONLY public.products DROP CONSTRAINT products_fk_id_state_fkey;
       public          postgres    false    217    227    3257            �           2606    34465 &   products products_fk_id_type_prod_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_fk_id_type_prod_fkey FOREIGN KEY (fk_id_type_prod) REFERENCES public.type_prods(id);
 P   ALTER TABLE ONLY public.products DROP CONSTRAINT products_fk_id_type_prod_fkey;
       public          postgres    false    225    227    3265            �           2606    34520    sales sales_fk_id_people_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_fk_id_people_fkey FOREIGN KEY (fk_id_people) REFERENCES public.peoples(id);
 G   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_fk_id_people_fkey;
       public          postgres    false    235    3259    219            �           2606    34515    sales sales_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 F   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_fk_id_state_fkey;
       public          postgres    false    217    3257    235            �           2606    34446 )   type_prods type_prods_fk_id_category_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.type_prods
    ADD CONSTRAINT type_prods_fk_id_category_fkey FOREIGN KEY (fk_id_category) REFERENCES public.categorys(id);
 S   ALTER TABLE ONLY public.type_prods DROP CONSTRAINT type_prods_fk_id_category_fkey;
       public          postgres    false    3263    225    223            �           2606    34427    users users_fk_id_people_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_fk_id_people_fkey FOREIGN KEY (fk_id_people) REFERENCES public.peoples(id);
 G   ALTER TABLE ONLY public.users DROP CONSTRAINT users_fk_id_people_fkey;
       public          postgres    false    221    219    3259            �           2606    34417    users users_fk_id_rol_fkey    FK CONSTRAINT     y   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_fk_id_rol_fkey FOREIGN KEY (fk_id_rol) REFERENCES public.rol(id);
 D   ALTER TABLE ONLY public.users DROP CONSTRAINT users_fk_id_rol_fkey;
       public          postgres    false    3255    215    221            �           2606    34422    users users_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 F   ALTER TABLE ONLY public.users DROP CONSTRAINT users_fk_id_state_fkey;
       public          postgres    false    221    217    3257            �      x������ � �      �      x������ � �      y   B   x�3��JM�+�2�tN��,N�2�H�+I����2�tN�)�I,�2�t��-(-IL�/J-����� ��A      �   Z   x�3�4�4�4�4202�5��50�t�*���".#NS���_jzQ>Tژ�$�,�Z��
�6�@7Yڔ�(�"�_��3=F��� �y D      �   �   x�m���0�P1���^�,'�,�$<���.3��S���/v�w>�M��_��s�w'HT; 쀀e�̕)	����8a����A�L��A����E0��Qe� �@l�̈́*�@�*�R%�M�F �N ��R�n
T�      �   *   x�3�t�I�O���2�tLN-�W��˯�LIL�I����� ��	�         F   x�3��2��2���2���2���2�4M�U�R04PH��2�44�q�rs�,8���\�l� ��      u   �   x���A�0��p
/ �i�����K15�%,<�G�b"�&���������q4G�%�[����֙3�&2�s�A�ftD�ZH!K	�錷>�@�)E	E�TY
v6����W$�
�G������_�0c�.��8�qZg�Q_��p=�Fہ��n�=�q�,1%L�$�Gҗ�/_�$I�`@e�      }   �   x�}�1�0�z9'�lJ++`�'N!^�#x1!h#�6�{��f� �Bv$�Y��U���zc�{>��������q?t���N 2��%l�r�(��*e��A9��e�D��&X�ʥZ7�4j�\|tޭH�o�a!�b�)�YQ���K2�#a�Y�u�Q�9{�������DQ�E�wD      q   :   x�3�tL����,.)JL�/�2�t�-�I���9���RSA�&��9��y%�\1z\\\ �n�      �   L   x�u�A� �5�E�A�x����M[]N^2b$d��V0
2� ˕ҷ�oqjx���V�(�+]�8��n�K����+"�      s   =   x�3�LN�KN�ILI�2�tL.�,��2���K�0M8]2���2�rR�L9��R�=... �E      {   x   x�]�;�0D�ڳ
� )��)J	��
��	,���&��54����4��O�g2I���&��;K�ɗ���`�p����b�h�yp���ʅ�5�����Ҏ/_����I���y���hq)e      w     x�m��n�@ ��5<�vD�`L�P���@,���
��-����E�x���[-~ҸӺ�zkwª �=���9�v�����l9O��&���q��EAE��]��q�Oįm�m��!��> }�� ��#N��<F�k�!}?��B��c����٨h�lo>+~��X�df�n�T<��T��Q���� ����U��'/_7�$V#��CZ�PY�$IFf�m\f/�z�(��F7)�I��%�69�cu���1A��<��dA     