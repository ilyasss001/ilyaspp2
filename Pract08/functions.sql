-- FUNCTION 1: SEARCH
CREATE OR REPLACE FUNCTION get_user_name_or_phone_number_by_pattern(p TEXT)
RETURNS TABLE(
    id INT,
    first_name TEXT,
    second_name TEXT,
    phone_number TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook2
    WHERE first_name ILIKE '%' || p || '%'
       OR second_name ILIKE '%' || p || '%'
       OR phone_number ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


-- FUNCTION 2: PAGINATION
CREATE OR REPLACE FUNCTION show_with_pagination(limit_val INT, offset_val INT)
RETURNS TABLE(
    id INT,
    first_name TEXT,
    second_name TEXT,
    phone_number TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook2
    ORDER BY id
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;