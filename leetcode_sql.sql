https://leetcode.com/problems/capital-gainloss/
'''1393. Capital Gain/Loss'''

with temp_temp as (
	select stock_name , 
		sum(case when operation = 'Buy' then price else 0 end )as buy_price ,
		sum(case when operation = 'Sell' then price else 0 end) as Sell_price 
	from stocks 
	group by stock_name 
) 
select stock_name , 
(Sell_price - buy_price ) as capital_gain_loss
from temp_temp;



''' 1407. Top Travellers '''
 https://leetcode.com/problems/top-travellers/


with temp_temp as (
	select u.id as user_id  ,
	coalesce(sum(r.distance),0)as travelled_distance 
	from users u 
	left join 	rides r on u.id = r.user_id 
	group by u.id 
	order by travelled_distance desc , 
		name asc 
) 
select e.name as name, 
t.travelled_distance as travelled_distance
from temp_temp t
left join users e on t.user_id = e.id ; 



'''1484. Group Sold Products By The Date'''
https://leetcode.com/problems/group-sold-products-by-the-date/



with temp_temp as (
	select sell_date , 
		count(distinct product) as num_sold ,  
		group_concat(distinct product order by product separator ',' ) as products
	from activities 
	group by sell_date 
	order by num_sold desc , product 
)
select sell_date,num_sold, products 
from temp_temp 
order by sell_date ; 
