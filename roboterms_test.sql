--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Company" (
    id integer NOT NULL,
    name character varying(80) NOT NULL,
    website character varying(80) NOT NULL
);


ALTER TABLE public."Company" OWNER TO postgres;

--
-- Name: Company_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Company_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Company_id_seq" OWNER TO postgres;

--
-- Name: Company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Company_id_seq" OWNED BY public."Company".id;


--
-- Name: Policy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Policy" (
    id integer NOT NULL,
    name character varying(80) NOT NULL,
    body character varying(3000) NOT NULL
);


ALTER TABLE public."Policy" OWNER TO postgres;

--
-- Name: Policy_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Policy_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Policy_id_seq" OWNER TO postgres;

--
-- Name: Policy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Policy_id_seq" OWNED BY public."Policy".id;


--
-- Name: Company id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Company" ALTER COLUMN id SET DEFAULT nextval('public."Company_id_seq"'::regclass);


--
-- Name: Policy id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Policy" ALTER COLUMN id SET DEFAULT nextval('public."Policy_id_seq"'::regclass);


--
-- Data for Name: Company; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Company" (id, name, website) FROM stdin;
1	Green Cola, Inc.	gcola.com
2	Googolplex AtoZ Data	stopdoingevilwheneverconvenient.com
3	Spy App Inc.	spyonyourlovedones--butlovingly.com
\.


--
-- Data for Name: Policy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Policy" (id, name, body) FROM stdin;
1	Terms of Service	\n        TERMS OF SERVICE\n\n        These Terms of Service ("Terms") govern your access to and use of the website "{WEBSITE}" and all its services.  Your access to and use of the Services are conditioned on your acceptance of and compliance with these Terms. By accessing or using the Services you agree to be bound by these Terms.\n\n        All Content, whether publicly posted or privately transmitted, is the sole responsibility of the person who originated such Content. You retain your rights to any Content you submit, post or display on or through the Services.\n\n        You are responsible for your use of the Services, for any Content you post to the Services, and for any consequences thereof.  {COMPANY} respects the intellectual property rights of others and expects users of the Services to do the same.\n\n        Your access to and use of the Services or any Content are at your own risk. You understand and agree that the Services are provided to you on an "AS IS" and "AS AVAILABLE" basis.\n\n        TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE ENTITIES SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL OR PUNITIVE DAMAGES, OR ANY LOSS OF PROFITS OR REVENUES, WHETHER INCURRED DIRECTLY OR INDIRECTLY, OR ANY LOSS OF DATA, USE, GOOD-WILL, OR OTHER INTANGIBLE LOSSES, RESULTING FROM (i) YOUR ACCESS TO OR USE OF OR INABILITY TO ACCESS OR USE THE SERVICES; (ii) ANY CONDUCT OR CONTENT OF ANY THIRD PARTY ON THE SERVICES, INCLUDING WITHOUT LIMITATION, ANY DEFAMATORY, OFFENSIVE OR ILLEGAL CONDUCT OF OTHER USERS OR THIRD PARTIES; (iii) ANY CONTENT OBTAINED FROM THE SERVICES; OR (iv) UNAUTHORIZED ACCESS, USE OR ALTERATION OF YOUR TRANSMISSIONS OR CONTENT.\n        
2	Cookies Policy	\n        COOKIES POLICY\n\n        {COMPANY} ("us", "we", or "our") uses cookies on "{WEBSITE}" (the "Service"). By using the Service, you consent to the use of cookies.\n\n        Our Cookies Policy explains what cookies are, how we use cookies, how third-parties we may partner with may use cookies on the Service, your choices regarding cookies and further information about cookies.\n\n        What are cookies\n\n        Cookies are small pieces of text sent by your web browser by a website you visit. A cookie file is stored in your web browser and allows the Service or a third-party to recognize you and make your next visit easier and the Service more useful to you.\n\n        Cookies can be "persistent" or "session" cookies.\n\n        How {COMPANY} uses cookies\n\n        When you use and access the Service, we may place a number of cookies files in your web browser.\n\n        We use cookies for the following purposes: to enable certain functions of the Service, to provide analytics, to store your preferences, to enable advertisements delivery, including behavioral advertising.\n\n        If you'd like to delete cookies or instruct your web browser to delete or refuse cookies, please visit the help pages of your web browser.\n\n        Please note, however, that if you delete cookies or refuse to accept them, you might not be able to use all of the features we offer, you may not be able to store your preferences, and some of our pages might not display properly.\n        
3	Disclaimer	\n        DISCLAIMER\n\n        This website {WEBSITE} owned and operated by {COMPANY} makes no representations as to accuracy, completeness, correctness, suitability, or validity of any information on this site and will not be liable for any errors, omissions, or delays in this information or any losses injuries, or damages arising from its display or use. All information is provided on an as-is basis.\n\n        The views and opinions expressed herein are those of the authors and do not necessarily reflect the official policy or position of any other agency, organization, employer or company.\n        
4	Privacy Policy	\n        PRIVACY POLICY\n\n        This statement ("Privacy Policy") covers the website {WEBSITE} owned and operated by {COMPANY} ("we", "us", "our") and all associated services.\n\n        We use information you share with us for our internal business purposes. We do not sell your information. This notice tells you what information we collect, how we use it, and steps we take to protect and secure it.\n\n        Information we automatically collect\n        Non-personally-identifying\n\n        Like most website operators, we collect non-personally-identifying information such as browser type, language preference, referring site, and the date and time of each visitor request.  We collect this to understand how our visitors use our service, and use it to make decisions about how to change and adapt the service.\n\n        From time to time, we may release non-personally-identifying information in aggregate form (for instance, by publishing trends in site usage) to explain our reasoning in making decisions. We will not release individual information, only aggregate information.\n\n        Personally-identifying\n\n        We automatically collect personally-identifying information, such as IP address, provided by your browser and your computer.\n\n        You can change or delete any optional information that you've provided us at any time. If you change or delete any optional information you've provided, the change will take place immediately.\n\n        You can also choose to delete your account entirely. If you choose to delete your account entirely, we will retain any personally-identifying information for a limited amount of time before removing it entirely. This is to allow you to undelete your account and continue using the service if you so choose. After this time, all your personally-identifying information will be removed entirely from our service, with the exception of any records we must retain to document compliance with regulatory requirements.\n        
\.


--
-- Name: Company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Company_id_seq"', 3, true);


--
-- Name: Policy_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Policy_id_seq"', 4, true);


--
-- Name: Company Company_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Company"
    ADD CONSTRAINT "Company_name_key" UNIQUE (name);


--
-- Name: Company Company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Company"
    ADD CONSTRAINT "Company_pkey" PRIMARY KEY (id);


--
-- Name: Company Company_website_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Company"
    ADD CONSTRAINT "Company_website_key" UNIQUE (website);


--
-- Name: Policy Policy_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Policy"
    ADD CONSTRAINT "Policy_name_key" UNIQUE (name);


--
-- Name: Policy Policy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Policy"
    ADD CONSTRAINT "Policy_pkey" PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

