//Highlights the appropriate DIV for the given aisle and side.
//Called by location_info.html
function new_highlight(library, floor, range, side)
{
	//alert("Called function with the following parameters: "+ library + ", " +floor+", "+range+", "+side);
	var divId = library+floor+range;
	//alert("DIV ID = "+divId);
	var activeDiv = document.getElementById(divId);
	var classToAdd;
	if (side == null || side == 'a')
		classToAdd = " activeA";
	else if (side == 'b')
		classToAdd = " activeB";
	else
	{
		alert("javascript: invalid side input: "+side);
		return;
	}
	
	activeDiv.className+=classToAdd;
}