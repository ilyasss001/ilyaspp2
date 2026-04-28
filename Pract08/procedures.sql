CREATE OR REPLACE PROCEDURE upsert_contact(p_1_name text, p_2_name text, p_phone_number text)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook2 WHERE first_name = p_1_name AND second_name = p_2_name) THEN
        UPDATE phonebook2 SET phone_number = p_phone_number WHERE first_name = p_1_name AND second_name = p_2_name;
    ELSE
        INSERT INTO phonebook2 (first_name, second_name, phone_number) VALUES(p_1_name, p_2_name, p_phone_number);
    END IF;
END;
$$;

CREATE PROCEDURE validate_phone_correctness(p_1_name TEXT[], p_2_name TEXT[], p_phone_number TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_1_name, 1) LOOP
        IF p_phone_number[i] ~ '^[+]{1}[0-9]{11}$' OR p_phone_number[i] ~ '^[8]{1}[0-9]{10}$' THEN
            INSERT INTO phonebook2 (first_name, second_name, phone_number) VALUES (p_1_name[i], p_2_name[i], p_phone_number[i]);
        ELSE
            RAISE NOTICE 'Invalid: %, %, %', p_1_name[i], p_2_name[i], p_phone_number[i];
        END IF;
    END LOOP;
END;
$$;

CREATE PROCEDURE delete_by_name_or_phonenumber(p TEXT)
AS $$
BEGIN
    DELETE FROM phonebook2
    WHERE first_name = p OR second_name = p OR phone_number = p;
END;
$$ LANGUAGE plpgsql;