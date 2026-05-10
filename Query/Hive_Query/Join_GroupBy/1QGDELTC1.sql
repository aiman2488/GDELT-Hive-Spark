select  a.Actor1Code, a.Actor1Name,
count (distinct a.GLOBALEVENTID) as EventCount,

sum (case when a.GoldsteinScale < -5 then 1 else 0 end) as HigherConflict,
sum (case when a.GoldsteinScale >= -5 and a.GoldsteinScale < 0 then 1 else 0 end) as LesserConflict,
sum (case when a.GoldsteinScale = 0 then 1 else 0 end) as Neutral,
sum (case when a.GoldsteinScale > 0 and a.GoldsteinScale <= 5 then 1 else 0 end) as LesserCooperation,
sum (case when a.GoldsteinScale > 5 then 1 else 0 end) as HigherCooperation,

round (
(sum (case when a.GoldsteinScale > 0 and a.GoldsteinScale <= 5 then 1 else 0 end) +
sum (case when a.GoldsteinScale > 5 then 1 else 0 end)) * 1.0 /
(sum (case when a.GoldsteinScale < -5 then 1 else 0 end) +
sum (case when a.GoldsteinScale >= -5 and a.GoldsteinScale < 0 then 1 else 0 end) + 1), 2
) as PolarityRatio

from <Table_Name> a
join <Table_Name> b 
on a.GLOBALEVENTID = b.GLOBALEVENTID

where a.Actor1Code is not NULL 
and b.Actor1Code is not NULL 
and trim (a.Actor1Name) != ''
and a.DATEADDED = 20260215
and b.DATEADDED = 20260215

group by a.Actor1Code, a.Actor1Name
order by EventCount desc limit 10;