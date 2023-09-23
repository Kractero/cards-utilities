#!/usr/bin/env python3

f = open('new_puppets_list.txt', 'r')
puppets = f.read().split('\n')
puppets = list(filter(None, puppets))
totalcount = len(puppets)

links = open('puppets_create.html', 'w')

links.write("""
<html>
<head>
<style>
td.createcol p {
	padding-left: 10em;
}

a {
	text-decoration: none;
	color: black;
}

a:visited {
	color: grey;
}

table {
	border-collapse: collapse;
	display: table-cell;
	max-width: 100%;
	border: 1px solid darkorange;
}

tr, td {
	border-bottom: 1px solid darkorange;
}

td p {
	padding: 0.5em;
}

tr:hover {
	background-color: lightgrey;
}

</style>
</head>
<body>
<table>
""")


for idx, k in enumerate(puppets):
	canonical = k.lower().replace(" ", "_")
	links.write("""<tr>""")
	links.write("""<td>{} of {}</td>""".format(idx+1, totalcount))
	links.write("""<td><p><a target="_blank" href="{}">Link to {}</a></p></td>""".format(f"https://www.nationstates.net/nation={canonical}/page=create_nation/name={k}", k))
	links.write("""</tr>\n""")


links.write("""<td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td><td><p><a target="_blank" href="https://this-page-intentionally-left-blank.org/">Done!</a></p></td>""".format(canonical))
links.write("""
</table>
<script>
document.querySelectorAll("td").forEach(function(el) {
	el.addEventListener("click", function() {
		let myidx = 0;
		const row = el.parentNode;
		let child = el;
		while((child = child.previousElementSibling) != null) {
			myidx++;
		}
		row.nextElementSibling.childNodes[myidx].querySelector("p > a").focus();
		row.parentNode.removeChild(row);
	});
});
</script>
</body>
""")