//Author    :   狼Robot
//Contact   :   robot@k2046.cn
//Date      :   2008-04-19
//Explain   :   使Table可以点击排序.

function TableSorter(table)
{
    this.Table = this.$(table);
    if(this.Table.rows.length <= 1)
    {
        return;
    }
    var args = [];
    if(arguments.length > 1)
    {
        for(var x = 1; x < arguments.length; x++)
        {
            args.push(arguments[x]);
        }
    }
    this.Init(args);
}

TableSorter.prototype = {
    $ : function(element)
    {
        return document.getElementById(element);
    },
    Init : function(args)
    {
        this.Rows = [];
        this.Header = [];
        this.ViewState = [];
        this.LastSorted = null;
        this.NormalCss = "NormalCss";
        this.SortAscCss = "SortAscCss";
        this.SortDescCss = "SortDescCss";
        for(var x = 0; x < this.Table.rows.length; x++)
        {
            this.Rows.push(this.Table.rows[x]);
        }
        this.Header = this.Rows.shift().cells;
        for(var x = 0; x < (args.length ? args.length : this.Header.length); x++)
        {
            var rowIndex = args.length ? args[x] : x;
            if(rowIndex >= this.Header.length)
            {
                continue;
            }
            this.ViewState[rowIndex] = false;
            this.Header[rowIndex].style.cursor = "pointer";
            this.Header[rowIndex].onclick = this.GetFunction(this, "Sort", rowIndex);
        }
    },
    GetFunction : function(variable,method,param)
    {
        return function()
        {
            variable[method](param);
        }
    },
    Sort : function(column)
    {
        if(this.LastSorted)
        {
            this.LastSorted.className = this.NormalCss;
        }
        var SortAsNumber = true;
        for(var x = 0; x < this.Rows.length && SortAsNumber; x++)
        {
            SortAsNumber = this.IsNumeric(this.Rows[x].cells[column].innerHTML);
        }
        this.Rows.sort(
        function(row1, row2)
        {
            var result;
            var value1,value2;
            value1 = row1.cells[column].innerHTML;
            value2 = row2.cells[column].innerHTML;
            if(value1 == value2)
            {
                return 0;
            }
            if(SortAsNumber)
            {
                result = parseFloat(value1) > parseFloat(value2);
            }
            else
            {
                result = value1 > value2;
            }
            result = result ? 1 : -1;
            return result;
        })
        if(this.ViewState[column])
        {
            this.Rows.reverse();
            this.ViewState[column] = false;
            this.Header[column].className = this.SortDescCss;
        }
        else
        {
            this.ViewState[column] = true;
            this.Header[column].className = this.SortAscCss;
        }
        this.LastSorted = this.Header[column];
        var frag = document.createDocumentFragment();
        for(var x = 0; x < this.Rows.length; x++)
        {
            frag.appendChild(this.Rows[x]);
        }
        this.Table.tBodies[0].appendChild(frag);
        this.OnSorted(this.Header[column], this.ViewState[column]);
    },
    IsNumeric : function(num)
    {
        return /^\d+(\.\d+)?$/.test(num);
    },
    OnSorted : function(cell, IsAsc)
    {
        return;
    }
}