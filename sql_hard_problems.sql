

''' sql  problems ''' 
''' Problem 1: Moving Average Anomaly Detection
You have a table containing daily transaction amounts for users. 
Your task is to find all transactions where the amount is more than 3 standard deviations away from the 30-day moving average.
''' 

WITH rolling_temp AS (
    SELECT 
        user_id, 
        transaction_date, 
        amount, 
        AVG(amount) OVER (
            PARTITION BY user_id 
            ORDER BY transaction_date 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_mean, 
        STDDEV(amount) OVER (
            PARTITION BY user_id 
            ORDER BY transaction_date 
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_std
    FROM transactions 
) 
SELECT 
    user_id, 
    transaction_date, 
    amount, 
    rolling_mean,
    rolling_std
FROM rolling_temp 
WHERE ABS(amount - rolling_mean) > 3 * rolling_std;
 

''' Problem 2: Churn Prediction Feature Engineering
Given a table of user logins, compute the churn score of each user. The churn score is defined as:

CREATE TABLE logins (
    user_id INT,
    login_date DATE
);
Task:
For each user, compute:

The number of days since their last login.
The average time between their logins.
The churn score.'''

WITH temp_temp AS (
    SELECT 
        user_id,
        login_date,
        MAX(login_date) OVER(PARTITION BY user_id) AS last_login, 
        
        -- Days since last login (only for the most recent login per user)
        DATEDIFF(
            MAX(login_date) OVER(PARTITION BY user_id),
            LAG(login_date) OVER(PARTITION BY user_id ORDER BY login_date)
        ) AS days_since_last_login,

        -- Average time between logins (NULL if only one login)
        CASE 
            WHEN COUNT(login_date) OVER(PARTITION BY user_id) = 1 THEN NULL
            ELSE AVG(DATEDIFF(login_date, LAG(login_date) OVER(PARTITION BY user_id ORDER BY login_date)))
                 OVER(PARTITION BY user_id)
        END AS avg_time_between_login
        
    FROM user_logins
)

SELECT 
    user_id, 
    last_login, 
    days_since_last_login, 
    avg_time_between_login, 
    ROUND(days_since_last_login / avg_time_between_login, 3) AS churn_score
FROM temp_temp;
