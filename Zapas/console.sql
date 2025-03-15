USE AdventureWorks2014

SELECT * FROM Person.Person

USE master
--na dole: select ALL from ...
SELECT * FROM AdventureWorks2014.Person.Person
--select kolumny productid, name, product number etc from SCHEMAT Production
SELECT Name, Color, ProductNumber, ProductID
FROM Production.Product
ORDER BY Color DESC, Name --kolumna o wartosci NULL zostanie podana na poczatku
--dane uporzadkowane alfabetycznie po nazwie w sposob rosnacy (czyli ASC, nie trzeba tego pisac bo to automatyczny sposob)
--bedziesz mial kolejnosc taka, w jakiej dales kolumny
--DESC czyli sposob malejacy po KOLORZE ale po NAZWIE mamy sposob rosnacy (automatyczny)

--przefiltrujemy zeby byly tylko produkty czarne
SELECT ProductID, Name, Color FROM Production.Product
WHERE Color = 'Black' --wynik 93 wierszy!

SELECT ProductID, Name, Color FROM Production.Product
WHERE ProductID = 317 --wynik 1 wiersz

--rok-miesiac-dzien godziny:minuty:sekundy.milisekundy
SELECT SellStartDate, Name, Color FROM Production.Product
WHERE SellStartDate = '2008-04-30 00:00:00' --wynik 211 wierszy, jesli nie podasz godziny to tez bedzie dzialas, ale musisz uzywac calego pelnego formatu np. kompletny format dat (jak napiszesz 2008 to nie zadziala) lub kompletny format godziny (jak dasz godziny i minuty ale nie sekundy to tez nie pojdzie) itp. itd.

-- <, >, <=, != znaki mniejszy, wiekszy, wiekszy lub rowny, inny od
SELECT ProductID, Name, Color FROM Production.Product
WHERE ProductID <= 317 -- > >=

SELECT ProductID, Name, Color FROM Production.Product
WHERE Color != 'Black' --wszystkie rozne od black

SELECT ProductID, Name, Color FROM Production.Product
WHERE Color LIKE 'Black' --szuka wszystkich ciągów znaków z wyrazem BLACK

SELECT ProductID, Name, Color FROM Production.Product
WHERE Name LIKE 'Half-Finger Gloves, _' -- dostajemy kazde Half-Finger Gloves z dodatkowym znakiem dzieki temu _

SELECT ProductID, Name, Color FROM Production.Product
WHERE Name LIKE 'Half-Finger Gloves, [M-Z]' -- jak u gory, ale mamy zakres

--operator OR
SELECT ProductID, Name, Color FROM Production.Product
WHERE Color ='Black' OR Color = 'Red' --produkty kolor czarnego lub czerwonego

--operator AND
SELECT ProductSubcategoryID, Name, Color FROM Production.Product
WHERE Color ='Black' OR Color = 'Red' AND ProductSubcategoryID = 14
--przy uzywaniu operatorow, jak OR i AND, musimy uwazac bo AND wykonuje sie przed OR,
--czyli tutaj to oznacza ze mamy CZARNE albo CZERWONE z SUBCATEGORY 14, jak to obejsc?
--uzyj NAWIASOW

SELECT ProductSubcategoryID, Name, Color FROM Production.Product
WHERE (Color ='Black' OR Color = 'Red') AND ProductSubcategoryID = 14 --teraz jest OK

SELECT ProductSubcategoryID, Name, Color FROM Production.Product
WHERE ProductSubcategoryID = 14 AND NOT Color = 'Black' --14 i nie Black

SELECT ProductSubcategoryID, Name, Color FROM Production.Product
WHERE Color ='Black'
   OR Color = 'Red'
   OR Color = 'Blue' --zamiast pisac OR mamy operator IN jak na dole

SELECT ProductSubcategoryID, Name, Color
FROM Production.Product
WHERE Color IN ('Black', 'Blue', 'Red')

SELECT ProductSubcategoryID, Name, Color
FROM Production.Product
WHERE Color NOT IN ('Black', 'Blue', 'Red')

SELECT ProductSubcategoryID, Name, Color
FROM Production.Product
WHERE ProductSubcategoryID >= 10
AND ProductSubcategoryID < 20

SELECT ProductSubcategoryID, Name, Color
FROM Production.Product
WHERE ProductSubcategoryID BETWEEN 10 AND 19

SELECT ProductSubcategoryID, SellStartDate, Name, Color
FROM Production.Product
    WHERE SellStartDate BETWEEN '2011-05-31' AND '2012-05-30'

SELECT ProductSubcategoryID, SellStartDate, Name, Color
FROM Production.Product
    WHERE SellStartDate >= '2011-05-31' AND SellStartDate <= '2012-05-30'

--IS
--IS NOT
SELECT ProductSubcategoryID, SellStartDate, Name, Color
FROM Production.Product
WHERE Color IS NULL --wszystkie produkty z wartoscia NULL

SELECT ProductSubcategoryID, SellStartDate, Name, Color
FROM Production.Product
WHERE Color IS NOT NULL --wszystkie produkty ktore nie sa z wartoscia NULL

--T-SQL czyli TRANSACT-SQL
SELECT Name, Color, ISNULL(Color, 'No color') AS SuperColor --funkcja ISNULL z kolumna COLOR i wyswietlanie No Color,
-- tam gdzie nie bylo color w SuperColor jest No color, tam gdzie byl Color to on jest powielany w SuperColor
FROM Production.Product

--w ten sposob otrzym tylko pojedyncze wystapienie kazdego koloru: DANE UNIKATOWE
SELECT DISTINCT Color FROM Production.Product

SELECT Name AS new_name, Color AS 'new color' FROM Production.Product --uzywajac slow w '' masz z przerwa, inaczej musisz pisac _ miedzy slowami

SELECT Name AS new_name, Color AS new_color FROM Production.Product

SELECT TOP 10 Name AS new_name, Color AS new_color FROM Production.Product --wynik 10
SELECT TOP 10 PERCENT Name AS new_name, Color AS new_color FROM Production.Product --wynik 10%

SELECT FirstName, LastName, FirstName + ' ' + LastName AS FullName --konkatenacja wartosci, mamy polaczenie Iminia i Nazwiska czyli FullName
FROM Person.Person

--T-SQL czyli T-SQL jest kompatybilny z Microsoft SQL Server Management Studio
SELECT FirstName,
    LEFT(FirstName, 1) AS FirstLetter, --wyciaga dane od lewej strony, first NAME i ILE ZNAKOW MA BRAC
    LEFT(FirstName, 3) AS First3Letters,
    RIGHT(FirstName, 1) AS LastLetter,
    SUBSTRING(FirstName, 1, 2),
    SUBSTRING(FirstName, 1, 4)
FROM Person.Person

--T-SQL
--jak wyciagnac rok z daty
--DATEDIFF(yy, SellStartDate, GETDATE()) mamy funkcje w funkcji
SELECT SellStartDate,
       YEAR(SellStartDate) AS Year,
       DATENAME(mm, SellStartDate) AS Month,
       DATENAME(dw, SellStartDate) AS WeekDay,
       DAY(SellStartDate),
       DATEDIFF(yy, SellStartDate, GETDATE())
FROM Production.Product
SET LANGUAGE 'Polish' --tłumaczy na polski

--inner join
SELECT p.Name, Color, psc.Name
FROM Production.Product p
JOIN Production.ProductSubcategory psc --mozesz tez zostawic JOIN bo to jest interpretowane jako defaultowane INNER JOIN
ON p.ProductSubCategoryID = psc.ProductSubCategoryID


SELECT p.Name, p.Color, psc.Name
FROM Production.Product p
    JOIN Production.ProductSubcategory psc --mozesz tez zostawic JOIN bo to jest interpretowane jako defaultowane INNER JOIN
        ON p.ProductSubCategoryID = psc.ProductSubCategoryID
    JOIN Production.ProductSubcategory pc
        ON psc.ProductCategoryID = pc.ProductCategoryID

SELECT psc.Name, pc.Name
FROM Production.Product p
    JOIN Production.ProductSubcategory psc --mozesz tez zostawic JOIN bo to jest interpretowane jako defaultowane INNER JOIN
        ON p.ProductSubCategoryID = psc.ProductSubCategoryID
    JOIN Production.ProductSubcategory pc
        ON psc.ProductCategoryID = pc.ProductCategoryID
WHERE YEAR(p.SellStartDate) > 2010

SELECT p.Name, p.Color, psc.Name AS SubcategoryName, pc.Name AS CategoryName
FROM Production.Product p
    JOIN Production.ProductSubcategory psc -- możesz zostawić JOIN jako domyślne INNER JOIN
        ON p.ProductSubCategoryID = psc.ProductSubCategoryID
    JOIN Production.ProductCategory pc
        ON psc.ProductCategoryID = pc.ProductCategoryID
WHERE pc.Name LIKE '%Clo%'
ORDER BY psc.Name DESC --powinno pokazac 35 linii produktow

SELECT p.Name, p.ProductSubcategoryID, psc.Name
FROM Production.Product p
LEFT JOIN Production.ProductSubcategory psc
    ON p.ProductSubcategoryID =  psc.ProductSubcategoryID


-- Grupowanie i funkcje agregujące
SELECT COUNT(*)                          AS ProductCnt,
       COUNT(ProductSubcategoryID)       AS Subcategories,
       AVG(Weight)                       AS AvgWeight, -- average, średnia
       MAX(Weight)                       AS MaxWeight,
       MIN(Weight)                       AS MinWeight
FROM Production.Product

SELECT Color, COUNT(*)
FROM Production.Product
GROUP BY Color
ORDER BY Color

SELECT p.Color, psc.Name, COUNT(*) AS ProductCnt --byla kolumna <anonymous> a teraz w wynikach bedzie ProductCnt
FROM Production.Product p
INNER JOIN Production.ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
WHERE p.Color IS NOT NULL -- != <>
GROUP BY p.Color, psc.Name
ORDER BY p.Color
--tu mamy mniej kolorow i mamy null bo pewnie te nie mialy zadnej subcategory

SELECT p.Color, psc.Name, COUNT(*) AS ProductCnt --byla kolumna <anonymous> a teraz w wynikach bedzie ProductCnt
FROM Production.Product p
INNER JOIN Production.ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
WHERE p.Color IS NOT NULL -- != <>
GROUP BY p.Color, psc.Name
ORDER BY ProductCnt DESC
--tu mamy mniej kolorow i mamy null bo pewnie te nie mialy zadnej subcategory

SELECT p.Color, psc.Name, COUNT(*) AS ProductCnt --byla kolumna <anonymous> a teraz w wynikach bedzie ProductCnt
FROM Production.Product p
INNER JOIN Production.ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
WHERE p.Color IS NOT NULL -- != <>
GROUP BY p.Color, psc.Name
HAVING COUNT(*) > 10
ORDER BY ProductCnt DESC
--tu mamy mniej kolorow i mamy null bo pewnie te nie mialy zadnej subcategory