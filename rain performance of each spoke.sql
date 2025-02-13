WITH cte AS (
    SELECT
        YEAR(date) AS year,
        MONTH(date) AS month,
        spoke,  

        ROUND(COALESCE(AVG(CASE WHEN working_precipitation <= 0.3 THEN net END), 0), 2) AS non_rainy_net_monthly,

        ROUND(COALESCE(AVG(CASE WHEN working_precipitation > 0.3 THEN net END), 0), 2) AS rainy_net_monthly,
        
        ROUND(COALESCE(AVG(CASE WHEN working_precipitation <=0.3 THEN discount END), 0), 2) AS non_rainy_discount_monthly,

        ROUND(COALESCE(AVG(CASE WHEN working_precipitation > 0.3 THEN discount END), 0), 2) AS rainy_discount_monthly
        
    FROM train  
--     where year(date) = 2023
    GROUP BY YEAR(date), MONTH(date), spoke  
)

SELECT
    spoke AS location,
    
    AVG(rainy_net_monthly) AS total_rainy_net,
    AVG(non_rainy_net_monthly) AS total_non_rainy_net,

    AVG(rainy_discount_monthly) AS avg_rainy_discount,
    AVG(non_rainy_discount_monthly) AS avg_non_rainy_discount,

    CASE 
        WHEN AVG(rainy_net_monthly) > 0 
        THEN ROUND((AVG(rainy_discount_monthly) / AVG(rainy_net_monthly)) * 100, 2) 
        ELSE NULL 
    END AS rainy_discount_rate,

    CASE 
        WHEN AVG(non_rainy_net_monthly) > 0 
        THEN ROUND((AVG(non_rainy_discount_monthly) / AVG(non_rainy_net_monthly)) * 100, 2) 
        ELSE NULL 
    END AS non_rainy_discount_rate,

    -- Percentage difference: (rainy - non-rainy) / non-rainy * 100
    CASE 
        WHEN AVG(non_rainy_net_monthly) > 0 
        THEN ROUND(((SUM(rainy_net_monthly) - SUM(non_rainy_net_monthly)) / SUM(non_rainy_net_monthly)) * 100, 2)
        ELSE NULL
    END AS net_percentage_difference,
    
    CASE 
        WHEN AVG(non_rainy_discount_monthly) > 0
        THEN ROUND(((SUM(rainy_discount_monthly) - SUM(non_rainy_discount_monthly)) / SUM(non_rainy_discount_monthly)) * 100, 2)
        ELSE NULL
    END AS discount_percentage_difference
    
FROM cte
GROUP BY spoke
ORDER BY spoke;
