PGDMP     *                    {         
   EcommerceM    15.3    15.3 e    w           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            x           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            y           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            z           1262    34067 
   EcommerceM    DATABASE     �   CREATE DATABASE "EcommerceM" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Colombia.1252';
    DROP DATABASE "EcommerceM";
                postgres    false            �            1259    34112 	   categorys    TABLE     [   CREATE TABLE public.categorys (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.categorys;
       public         heap    postgres    false            �            1259    34111    categorys_id_seq    SEQUENCE     �   CREATE SEQUENCE public.categorys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.categorys_id_seq;
       public          postgres    false    221            {           0    0    categorys_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.categorys_id_seq OWNED BY public.categorys.id;
          public          postgres    false    220            �            1259    34242    detail_prods    TABLE     �   CREATE TABLE public.detail_prods (
    id integer NOT NULL,
    fk_id_product integer,
    fk_id_measures integer,
    fk_id_materials integer,
    date date DEFAULT CURRENT_DATE NOT NULL,
    color character varying(30)
);
     DROP TABLE public.detail_prods;
       public         heap    postgres    false            �            1259    34241    detail_prods_id_seq    SEQUENCE     �   CREATE SEQUENCE public.detail_prods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.detail_prods_id_seq;
       public          postgres    false    233            |           0    0    detail_prods_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.detail_prods_id_seq OWNED BY public.detail_prods.id;
          public          postgres    false    232            �            1259    34265    detail_sales    TABLE     �   CREATE TABLE public.detail_sales (
    id integer NOT NULL,
    fk_id_sale integer,
    fk_id_prod integer,
    quantity integer,
    price_unit numeric(10,2),
    total_product numeric(10,2)
);
     DROP TABLE public.detail_sales;
       public         heap    postgres    false            �            1259    34264    detail_sales_id_seq    SEQUENCE     �   CREATE SEQUENCE public.detail_sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.detail_sales_id_seq;
       public          postgres    false    235            }           0    0    detail_sales_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.detail_sales_id_seq OWNED BY public.detail_sales.id;
          public          postgres    false    234            �            1259    34157 	   materials    TABLE     [   CREATE TABLE public.materials (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.materials;
       public         heap    postgres    false            �            1259    34156    materials_id_seq    SEQUENCE     �   CREATE SEQUENCE public.materials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.materials_id_seq;
       public          postgres    false    227            ~           0    0    materials_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.materials_id_seq OWNED BY public.materials.id;
          public          postgres    false    226            �            1259    34150    measures    TABLE     Z   CREATE TABLE public.measures (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.measures;
       public         heap    postgres    false            �            1259    34149    measures_id_seq    SEQUENCE     �   CREATE SEQUENCE public.measures_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.measures_id_seq;
       public          postgres    false    225                       0    0    measures_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.measures_id_seq OWNED BY public.measures.id;
          public          postgres    false    224            �            1259    34083    peoples    TABLE     �  CREATE TABLE public.peoples (
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
    is_empleado boolean,
    is_cliente boolean
);
    DROP TABLE public.peoples;
       public         heap    postgres    false            �            1259    34082    peoples_id_seq    SEQUENCE     �   CREATE SEQUENCE public.peoples_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.peoples_id_seq;
       public          postgres    false    219            �           0    0    peoples_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.peoples_id_seq OWNED BY public.peoples.id;
          public          postgres    false    218            �            1259    34223    products    TABLE     R  CREATE TABLE public.products (
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
       public         heap    postgres    false            �            1259    34222    products_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.products_id_seq;
       public          postgres    false    231            �           0    0    products_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;
          public          postgres    false    230            �            1259    34069    rol    TABLE     U   CREATE TABLE public.rol (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.rol;
       public         heap    postgres    false            �            1259    34068 
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
          public          postgres    false    214            �            1259    34187    sales    TABLE     �   CREATE TABLE public.sales (
    id integer NOT NULL,
    fk_id_state integer,
    fk_id_people integer,
    date date DEFAULT CURRENT_DATE NOT NULL,
    total_sale numeric(10,2)
);
    DROP TABLE public.sales;
       public         heap    postgres    false            �            1259    34186    sales_id_seq    SEQUENCE     �   CREATE SEQUENCE public.sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.sales_id_seq;
       public          postgres    false    229            �           0    0    sales_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.sales_id_seq OWNED BY public.sales.id;
          public          postgres    false    228            �            1259    34076    states    TABLE     X   CREATE TABLE public.states (
    id integer NOT NULL,
    name character varying(30)
);
    DROP TABLE public.states;
       public         heap    postgres    false            �            1259    34075    states_id_seq    SEQUENCE     �   CREATE SEQUENCE public.states_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.states_id_seq;
       public          postgres    false    217            �           0    0    states_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.states_id_seq OWNED BY public.states.id;
          public          postgres    false    216            �            1259    34119 
   type_prods    TABLE     x   CREATE TABLE public.type_prods (
    id integer NOT NULL,
    fk_id_category integer,
    name character varying(30)
);
    DROP TABLE public.type_prods;
       public         heap    postgres    false            �            1259    34118    type_prods_id_seq    SEQUENCE     �   CREATE SEQUENCE public.type_prods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.type_prods_id_seq;
       public          postgres    false    223            �           0    0    type_prods_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.type_prods_id_seq OWNED BY public.type_prods.id;
          public          postgres    false    222            �            1259    34282    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    fk_id_state integer,
    fk_id_rol integer,
    fk_id_people integer,
    password character varying(100),
    last_login timestamp without time zone
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    34281    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    237            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    236            �           2604    34115    categorys id    DEFAULT     l   ALTER TABLE ONLY public.categorys ALTER COLUMN id SET DEFAULT nextval('public.categorys_id_seq'::regclass);
 ;   ALTER TABLE public.categorys ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    221    220    221            �           2604    34245    detail_prods id    DEFAULT     r   ALTER TABLE ONLY public.detail_prods ALTER COLUMN id SET DEFAULT nextval('public.detail_prods_id_seq'::regclass);
 >   ALTER TABLE public.detail_prods ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    232    233    233            �           2604    34268    detail_sales id    DEFAULT     r   ALTER TABLE ONLY public.detail_sales ALTER COLUMN id SET DEFAULT nextval('public.detail_sales_id_seq'::regclass);
 >   ALTER TABLE public.detail_sales ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    235    234    235            �           2604    34160    materials id    DEFAULT     l   ALTER TABLE ONLY public.materials ALTER COLUMN id SET DEFAULT nextval('public.materials_id_seq'::regclass);
 ;   ALTER TABLE public.materials ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    227    227            �           2604    34153    measures id    DEFAULT     j   ALTER TABLE ONLY public.measures ALTER COLUMN id SET DEFAULT nextval('public.measures_id_seq'::regclass);
 :   ALTER TABLE public.measures ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    225    224    225            �           2604    34086 
   peoples id    DEFAULT     h   ALTER TABLE ONLY public.peoples ALTER COLUMN id SET DEFAULT nextval('public.peoples_id_seq'::regclass);
 9   ALTER TABLE public.peoples ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    219    219            �           2604    34226    products id    DEFAULT     j   ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);
 :   ALTER TABLE public.products ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    231    231            �           2604    34072    rol id    DEFAULT     `   ALTER TABLE ONLY public.rol ALTER COLUMN id SET DEFAULT nextval('public.rol_id_seq'::regclass);
 5   ALTER TABLE public.rol ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214    215            �           2604    34190    sales id    DEFAULT     d   ALTER TABLE ONLY public.sales ALTER COLUMN id SET DEFAULT nextval('public.sales_id_seq'::regclass);
 7   ALTER TABLE public.sales ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    229    228    229            �           2604    34079 	   states id    DEFAULT     f   ALTER TABLE ONLY public.states ALTER COLUMN id SET DEFAULT nextval('public.states_id_seq'::regclass);
 8   ALTER TABLE public.states ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216    217            �           2604    34122    type_prods id    DEFAULT     n   ALTER TABLE ONLY public.type_prods ALTER COLUMN id SET DEFAULT nextval('public.type_prods_id_seq'::regclass);
 <   ALTER TABLE public.type_prods ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    223    222    223            �           2604    34285    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    236    237    237            d          0    34112 	   categorys 
   TABLE DATA           -   COPY public.categorys (id, name) FROM stdin;
    public          postgres    false    221   ?r       p          0    34242    detail_prods 
   TABLE DATA           g   COPY public.detail_prods (id, fk_id_product, fk_id_measures, fk_id_materials, date, color) FROM stdin;
    public          postgres    false    233   xr       r          0    34265    detail_sales 
   TABLE DATA           g   COPY public.detail_sales (id, fk_id_sale, fk_id_prod, quantity, price_unit, total_product) FROM stdin;
    public          postgres    false    235   �r       j          0    34157 	   materials 
   TABLE DATA           -   COPY public.materials (id, name) FROM stdin;
    public          postgres    false    227   as       h          0    34150    measures 
   TABLE DATA           ,   COPY public.measures (id, name) FROM stdin;
    public          postgres    false    225   �s       b          0    34083    peoples 
   TABLE DATA           �   COPY public.peoples (id, email, name, last_name, type_document, document, gender, date_birth, phone, address, is_empleado, is_cliente) FROM stdin;
    public          postgres    false    219   't       n          0    34223    products 
   TABLE DATA           �   COPY public.products (id, fk_id_state, fk_id_type_prod, name, image, reference, description, quantity, price_shop, price_sale) FROM stdin;
    public          postgres    false    231   u       ^          0    34069    rol 
   TABLE DATA           '   COPY public.rol (id, name) FROM stdin;
    public          postgres    false    215   ;v       l          0    34187    sales 
   TABLE DATA           P   COPY public.sales (id, fk_id_state, fk_id_people, date, total_sale) FROM stdin;
    public          postgres    false    229   |v       `          0    34076    states 
   TABLE DATA           *   COPY public.states (id, name) FROM stdin;
    public          postgres    false    217   �v       f          0    34119 
   type_prods 
   TABLE DATA           >   COPY public.type_prods (id, fk_id_category, name) FROM stdin;
    public          postgres    false    223   'w       t          0    34282    users 
   TABLE DATA           _   COPY public.users (id, fk_id_state, fk_id_rol, fk_id_people, password, last_login) FROM stdin;
    public          postgres    false    237   yw       �           0    0    categorys_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.categorys_id_seq', 3, true);
          public          postgres    false    220            �           0    0    detail_prods_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.detail_prods_id_seq', 12, true);
          public          postgres    false    232            �           0    0    detail_sales_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.detail_sales_id_seq', 16, true);
          public          postgres    false    234            �           0    0    materials_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.materials_id_seq', 5, true);
          public          postgres    false    226            �           0    0    measures_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.measures_id_seq', 9, true);
          public          postgres    false    224            �           0    0    peoples_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.peoples_id_seq', 14, true);
          public          postgres    false    218            �           0    0    products_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.products_id_seq', 23, true);
          public          postgres    false    230            �           0    0 
   rol_id_seq    SEQUENCE SET     8   SELECT pg_catalog.setval('public.rol_id_seq', 4, true);
          public          postgres    false    214            �           0    0    sales_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.sales_id_seq', 14, true);
          public          postgres    false    228            �           0    0    states_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.states_id_seq', 7, true);
          public          postgres    false    216            �           0    0    type_prods_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.type_prods_id_seq', 5, true);
          public          postgres    false    222            �           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 8, true);
          public          postgres    false    236            �           2606    34117    categorys categorys_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.categorys
    ADD CONSTRAINT categorys_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.categorys DROP CONSTRAINT categorys_pkey;
       public            postgres    false    221            �           2606    34248    detail_prods detail_prods_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_pkey;
       public            postgres    false    233            �           2606    34270    detail_sales detail_sales_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.detail_sales
    ADD CONSTRAINT detail_sales_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.detail_sales DROP CONSTRAINT detail_sales_pkey;
       public            postgres    false    235            �           2606    34162    materials materials_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.materials DROP CONSTRAINT materials_pkey;
       public            postgres    false    227            �           2606    34155    measures measures_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.measures
    ADD CONSTRAINT measures_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.measures DROP CONSTRAINT measures_pkey;
       public            postgres    false    225            �           2606    34088    peoples peoples_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.peoples
    ADD CONSTRAINT peoples_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.peoples DROP CONSTRAINT peoples_pkey;
       public            postgres    false    219            �           2606    34230    products products_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public            postgres    false    231            �           2606    34074    rol rol_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id);
 6   ALTER TABLE ONLY public.rol DROP CONSTRAINT rol_pkey;
       public            postgres    false    215            �           2606    34193    sales sales_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_pkey;
       public            postgres    false    229            �           2606    34081    states states_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.states
    ADD CONSTRAINT states_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.states DROP CONSTRAINT states_pkey;
       public            postgres    false    217            �           2606    34124    type_prods type_prods_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.type_prods
    ADD CONSTRAINT type_prods_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.type_prods DROP CONSTRAINT type_prods_pkey;
       public            postgres    false    223            �           2606    34287    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    237            �           2606    34259 .   detail_prods detail_prods_fk_id_materials_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_fk_id_materials_fkey FOREIGN KEY (fk_id_materials) REFERENCES public.materials(id);
 X   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_fk_id_materials_fkey;
       public          postgres    false    3255    233    227            �           2606    34254 -   detail_prods detail_prods_fk_id_measures_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_fk_id_measures_fkey FOREIGN KEY (fk_id_measures) REFERENCES public.measures(id);
 W   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_fk_id_measures_fkey;
       public          postgres    false    3253    225    233            �           2606    34249 ,   detail_prods detail_prods_fk_id_product_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_prods
    ADD CONSTRAINT detail_prods_fk_id_product_fkey FOREIGN KEY (fk_id_product) REFERENCES public.products(id);
 V   ALTER TABLE ONLY public.detail_prods DROP CONSTRAINT detail_prods_fk_id_product_fkey;
       public          postgres    false    233    3259    231            �           2606    34276 )   detail_sales detail_sales_fk_id_prod_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_sales
    ADD CONSTRAINT detail_sales_fk_id_prod_fkey FOREIGN KEY (fk_id_prod) REFERENCES public.products(id);
 S   ALTER TABLE ONLY public.detail_sales DROP CONSTRAINT detail_sales_fk_id_prod_fkey;
       public          postgres    false    3259    235    231            �           2606    34271 )   detail_sales detail_sales_fk_id_sale_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.detail_sales
    ADD CONSTRAINT detail_sales_fk_id_sale_fkey FOREIGN KEY (fk_id_sale) REFERENCES public.sales(id);
 S   ALTER TABLE ONLY public.detail_sales DROP CONSTRAINT detail_sales_fk_id_sale_fkey;
       public          postgres    false    229    235    3257            �           2606    34231 "   products products_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 L   ALTER TABLE ONLY public.products DROP CONSTRAINT products_fk_id_state_fkey;
       public          postgres    false    231    217    3245            �           2606    34236 &   products products_fk_id_type_prod_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_fk_id_type_prod_fkey FOREIGN KEY (fk_id_type_prod) REFERENCES public.type_prods(id);
 P   ALTER TABLE ONLY public.products DROP CONSTRAINT products_fk_id_type_prod_fkey;
       public          postgres    false    231    3251    223            �           2606    34199    sales sales_fk_id_people_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_fk_id_people_fkey FOREIGN KEY (fk_id_people) REFERENCES public.peoples(id);
 G   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_fk_id_people_fkey;
       public          postgres    false    3247    219    229            �           2606    34194    sales sales_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 F   ALTER TABLE ONLY public.sales DROP CONSTRAINT sales_fk_id_state_fkey;
       public          postgres    false    3245    217    229            �           2606    34125 )   type_prods type_prods_fk_id_category_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.type_prods
    ADD CONSTRAINT type_prods_fk_id_category_fkey FOREIGN KEY (fk_id_category) REFERENCES public.categorys(id);
 S   ALTER TABLE ONLY public.type_prods DROP CONSTRAINT type_prods_fk_id_category_fkey;
       public          postgres    false    221    3249    223            �           2606    34298    users users_fk_id_people_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_fk_id_people_fkey FOREIGN KEY (fk_id_people) REFERENCES public.peoples(id);
 G   ALTER TABLE ONLY public.users DROP CONSTRAINT users_fk_id_people_fkey;
       public          postgres    false    3247    219    237            �           2606    34288    users users_fk_id_rol_fkey    FK CONSTRAINT     y   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_fk_id_rol_fkey FOREIGN KEY (fk_id_rol) REFERENCES public.rol(id);
 D   ALTER TABLE ONLY public.users DROP CONSTRAINT users_fk_id_rol_fkey;
       public          postgres    false    215    237    3243            �           2606    34293    users users_fk_id_state_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_fk_id_state_fkey FOREIGN KEY (fk_id_state) REFERENCES public.states(id);
 F   ALTER TABLE ONLY public.users DROP CONSTRAINT users_fk_id_state_fkey;
       public          postgres    false    237    3245    217            d   )   x�3�t�IM.)�O��=���$39��ˈ3(� �+F��� ͋
�      p   t   x�]�=
�0����)��Ҥ����	\D������� h%[^x�����G�m%6����!�J����99�i?�((����C}�-9��[����ɡV�Ԓ�G�ѹ6#��)      r   U   x�m�� !D�C1�ϊ���_�
dO�L���c�a�v�Ƶ�	�]I��~A4����<��#�)T{3��:���4�FD�X�      j   A   x�3�tLN-�W��˯�LIL�I�2�
�f��g&�s�p:��ޜ�e�铙\������ �\�      h   e   x�3�4H��Q0�f@�˘���@�BBI�Ģ��<�����TM.SNc�
C�
Cc#�dqj^rfNN�&�g0�%�/�9��g��	gD0W� ���      b   �   x���AN1���)�@�8鴓]GTe�t2)��h��k�Ћ��-#y�o���$u�|�\|�5Hٿd�:HƱ�~�x��<:����Ǒ�N,rN�H���6�6`	�kKG�@��|j�z��e�o>_'�ϕ1\8�8
������鶻����^��!M��B�C�B�}̘�;C��2g¬h���Bv1���y�����w      n   &  x�u�MN�0�דS�i=IEX����!�J�4U��ؘXp/���p	Z��h��� 	׬�&'<����������{{ 
ayuQ
������:T�����d��y���n��s�y���Ҙ�����L���4�v4�aAy4���ީ��r�_��v<��n��uʶ��sMɦ�}$.F��g#	��;G�`��;�Q��yAo����C1�f�;GZѫ�4��V�F��,h�&jc${���ZG.�n���#�U�:8���4�3t�pE.}m�wy�e�����      ^   1   x�3�tL����,.)JL�/�2�t��L�+I�2�t�-�I�r��qqq &�      l   O   x�u���0�7�bkY��^���<"�|gB(!�`R����<�w��w�<:���j8�e���9��������UU�Zk'�      `   <   x�3�t�,.���L�I�2���W@�s:&�d��s�pz�%B�f��\�@u�IE�\1z\\\ Ąx      f   B   x�3�4��I,KL�/J,�2�4�.MILI�<����� ���/�,c
ҕ�\
����� ��      t     x�m��n�@ ϻ_�7#Y�۷�x�E-���I�`���AHկ/����y�d�IFl�.�x?+ e�V5L�r�e�U�����rJ�jv��{M�3����8s�٭}�7�r�&��,\Fm>0�}�� 7 ��6)$@N�e�4˪��nv͟+/.(��m�$Gs������G���]i���g��0�s���2O_�i7�͎�Z$�DCiX�b�u���������0��K�؆$��a7�\�(�r�����-Q�����dTV�     