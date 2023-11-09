QTY_BY_WAREHOUSE = """
;

With CTE As (
    select
        tl.ITEMID,
        id.INVENTCOLORID,
        id.INVENTSIZEID,
        sum(tl.qtytransfer) as QtyNeeded
    from
        inventtransferline tl
        join inventtransfertable tt on tt.dataareaid = tl.dataareaid
        and tt.PARTITION = tl.PARTITION
        and tt.TRANSFERID = tl.TRANSFERID
        join inventdim id on id.DATAAREAID = tl.DATAAREAID
        and id.PARTITION = tl.PARTITION
        and id.INVENTDIMID = tl.INVENTDIMID
    where
        tt.inventlocationidto = 'XBR-R'
        and tt.TRANSFERSTATUS = 0
    group by
        tl.ITEMID,
        id.INVENTCOLORID,
        id.INVENTSIZEID
)
Select
    cte.*,
    isnull (
        (
            Select
                isum.AVAILPHYSICAL
            from
                inventsum isum
                join inventdim ID ON id.DATAAREAID = isum.DATAAREAID
                and id.PARTITION = isum.PARTITION
                and id.inventdimid = isum.INVENTDIMID
                and id.INVENTCOLORID = cte.INVENTCOLORID
                and id.INVENTSIZEID = cte.INVENTSIZEID
                and id.INVENTLOCATIONID = 'STL'
                and id.INVENTSITEID = 'KT'
            where
                isum.dataareaid = 'LAN'
                and isum.PARTITION = 5637144576
                and isum.itemid = cte.ITEMID
        ),
        0
    ) as STL_QTY,
    isnull(
        (
            Select
                isum.AVAILPHYSICAL
            from
                inventsum isum
                join inventdim ID ON id.DATAAREAID = isum.DATAAREAID
                and id.PARTITION = isum.PARTITION
                and id.inventdimid = isum.INVENTDIMID
                and id.INVENTCOLORID = cte.INVENTCOLORID
                and id.INVENTSIZEID = cte.INVENTSIZEID
                and id.INVENTLOCATIONID = 'STL-L'
                and id.INVENTSITEID = 'KT'
            where
                isum.dataareaid = 'LAN'
                and isum.PARTITION = 5637144576
                and isum.itemid = cte.ITEMID
        ),
        0
    ) as STL_L_QTY,
    isnull(
        (
            Select
                isum.AVAILPHYSICAL
            from
                inventsum isum
                join inventdim ID ON id.DATAAREAID = isum.DATAAREAID
                and id.PARTITION = isum.PARTITION
                and id.inventdimid = isum.INVENTDIMID
                and id.INVENTCOLORID = cte.INVENTCOLORID
                and id.INVENTSIZEID = cte.INVENTSIZEID
                and id.INVENTLOCATIONID = 'OB'
                and id.INVENTSITEID = 'OB'
            where
                isum.dataareaid = 'LAN'
                and isum.PARTITION = 5637144576
                and isum.itemid = cte.ITEMID
        ),
        0
    ) as OB_QTY,
    isnull(
        (
            Select
                isum.AVAILPHYSICAL
            from
                inventsum isum
                join inventdim ID ON id.DATAAREAID = isum.DATAAREAID
                and id.PARTITION = isum.PARTITION
                and id.inventdimid = isum.INVENTDIMID
                and id.INVENTCOLORID = cte.INVENTCOLORID
                and id.INVENTSIZEID = cte.INVENTSIZEID
                and id.INVENTLOCATIONID = 'OB-L'
                and id.INVENTSITEID = 'OB'
            where
                isum.dataareaid = 'LAN'
                and isum.PARTITION = 5637144576
                and isum.itemid = cte.ITEMID
        ),
        0
    ) as OB_L_QTY
from
    cte
order by
    cte.ITEMID,
    cte.INVENTCOLORID,
    cte.INVENTSIZEID
"""