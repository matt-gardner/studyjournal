function toggle_notes(id)
{
	var ob = document.getElementById(id);
	if (ob.className == 'hide_notes')
	{
		ob.className = 'show_notes';
	}
	else
	{
		ob.className = 'hide_notes';
	}
}
function toggle_all_notes(table_name)
{
	var table = document.getElementById(table_name);
	for (row in table.rows)
	{
		if (table.rows[row].className == 'hide_notes')
		{
			table.rows[row].className = 'show_notes';
		}
		else if (table.rows[row].className == 'show_notes')
		{
			table.rows[row].className = 'hide_notes';
		}
	}
}
function toggle_scriptures(book)
{
	var table = document.getElementById(book);
	if (table.className == 'scriptures_hide')
	{
		table.className = 'scriptures_show';
	}
	else
	{
		table.className = 'scriptures_hide';
	}
}
function confirm_delete(baseurl, name, deleteurl)
{
	var result = confirm("Are you sure you want to delete "+name+"?");
	if (result == true)
	{
		window.location=baseurl+"?delete="+deleteurl;
	}
	else
	{
	}
}
