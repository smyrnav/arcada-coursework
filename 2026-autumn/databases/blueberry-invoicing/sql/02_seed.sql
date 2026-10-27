-- Fabricated data for the assignment.
-- Invoices 1–3 stand in for the three ready-made invoices in the FileMaker file;
-- 4–20 are the new ones. Dates ascend through October–November 2026.
-- Status: invoices 1–10 Paid, 11–15 Sent, 16–20 Open.

PRAGMA foreign_keys = ON;

INSERT INTO customers (customer_id, company_name, street_address, postal_code, city, country, email, phone) VALUES
    (1, 'Smyrna V',                 'Jan-Magnus Janssonin aukio 1', '00560', 'Helsinki', 'Finland', 'smyrna.v@example.com', '+358 40 100 2001'),
    (2, 'Nordic Pixel Oy',           'Mannerheimintie 12 B',         '00100', 'Helsinki', 'Finland', 'orders@nordicpixel.fi',  '+358 9 555 0102'),
    (3, 'Kallio Coffee Lab',         'Vaasankatu 7',                 '00500', 'Helsinki', 'Finland', 'hello@kalliocoffee.fi',  '+358 44 555 0103'),
    (4, 'Espoo Robotics Club ry',    'Otakaari 24',                  '02150', 'Espoo',    'Finland', 'board@espoorobotics.fi', '+358 50 555 0104'),
    (5, 'Turku Sound & Light Ab',    'Linnankatu 31',                '20100', 'Turku',    'Finland', 'info@tsl.fi',            '+358 2 555 0105');

INSERT INTO items (item_id, item_name, category, description, price, stock) VALUES
    (1, 'BB-Pulse Wireless Earbuds',  'Audio',       'Bluetooth 5.3 earbuds with noise cancelling and charging case, 28 h battery.', 79.90,  140),
    (2, 'VoltCore 20W USB-C Charger', 'Accessories', 'Compact GaN wall charger, USB-C PD 20 W, EU plug.',                           24.50,  320),
    (3, 'ClearView 27" Monitor Arm',  'Office',      'Gas-spring single monitor arm for 17–27" screens, VESA 75/100, desk clamp.',  119.00,  45);

INSERT INTO invoices (invoice_number, customer_id, invoice_date, days_to_payment, status) VALUES
    ( 1, 2, '2026-10-02', 14, 'Paid'),
    ( 2, 3, '2026-10-05', 14, 'Paid'),
    ( 3, 4, '2026-10-07', 30, 'Paid'),
    ( 4, 5, '2026-10-09', 14, 'Paid'),
    ( 5, 1, '2026-10-12', 14, 'Paid'),
    ( 6, 2, '2026-10-14', 30, 'Paid'),
    ( 7, 3, '2026-10-16', 14, 'Paid'),
    ( 8, 4, '2026-10-19', 14, 'Paid'),
    ( 9, 5, '2026-10-21', 30, 'Paid'),
    (10, 2, '2026-10-23', 14, 'Paid'),
    (11, 3, '2026-10-26', 14, 'Sent'),
    (12, 1, '2026-10-28', 14, 'Sent'),
    (13, 4, '2026-10-30', 30, 'Sent'),
    (14, 5, '2026-11-02', 14, 'Sent'),
    (15, 2, '2026-11-04', 14, 'Sent'),
    (16, 3, '2026-11-06', 30, 'Open'),
    (17, 4, '2026-11-09', 14, 'Open'),
    (18, 5, '2026-11-11', 14, 'Open'),
    (19, 2, '2026-11-13', 30, 'Open'),
    (20, 1, '2026-11-16', 14, 'Open');

INSERT INTO invoice_rows (invoice_number, item_id, amount) VALUES
    ( 1, 1, 10), ( 1, 2, 10),
    ( 2, 2,  4),
    ( 3, 3,  6), ( 3, 2,  6),
    ( 4, 1, 25),
    ( 5, 1,  1), ( 5, 2,  1),
    ( 6, 3, 12),
    ( 7, 2,  8), ( 7, 1,  2),
    ( 8, 1,  5), ( 8, 2,  5), ( 8, 3, 1),
    ( 9, 3,  3),
    (10, 1, 15),
    (11, 2, 20),
    (12, 3,  1),
    (13, 1,  8), (13, 3,  2),
    (14, 2, 30), (14, 1,  4),
    (15, 3,  5),
    (16, 2,  6), (16, 1,  3),
    (17, 1, 12), (17, 2, 12), (17, 3, 2),
    (18, 3,  4),
    (19, 1, 20), (19, 2, 10),
    (20, 1,  2), (20, 2,  2), (20, 3, 1);
