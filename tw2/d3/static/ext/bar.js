
if ( typeof tw2 == "undefined" ) tw2 = {};
if ( typeof tw2.store == "undefined" ) tw2.store = {};
if ( typeof tw2.d3 == "undefined" ) tw2.d3 = {};

$.extend(tw2.d3, {
    bar: function (selector, data, width, height, padding, format) {
        var w = width - padding[1] - padding[3];
        var h = height - padding[0] - padding[2];

        var format = d3.format(format);

        var x = d3.scale.linear().range([0, w]),
        y = d3.scale.ordinal().rangeRoundBands([0, h], .1);

        var xAxis = d3.svg.axis().scale(x).orient("top").tickSize(-h),
        yAxis = d3.svg.axis().scale(y).orient("left").tickSize(0);

        $(document).ready(function() {
            var svg = d3.select("#" + selector).append("svg")
            .attr("width", w + padding[1] + padding[3])
            .attr("height", h + padding[0] + padding[2])
            .append("g")
            .attr("transform", "translate(" + padding[3] + "," + padding[0] + ")");

            // Parse numbers
            $.each(data, function(i, d) { d.value = +d.value; });

            // Set the scale domain.
            x.domain([0, d3.max(data, function(d) { return d.value; })]);
            y.domain($.map(data, function(d, i) { return d.key; }));

            var bar = svg.selectAll("g.bar")
            .data(data)
            .enter().append("g")
            .attr("class", "bar")
            .attr("transform", function(d) {
                return "translate(0," + y(d.key) + ")"; 
            });

            bar.append("rect")
            .attr("width", function(d) { return x(d.value); })
            .attr("height", y.rangeBand());

            bar.append("text")
            .attr("class", "value")
            .attr("x", function(d) { return x(d.value); })
            .attr("y", y.rangeBand() / 2)
            .attr("dx", -3)
            .attr("dy", ".35em")
            .attr("text-anchor", "end")
            .text(function(d) { return format(d.value); });

            svg.append("g")
            .attr("class", "x axis")
            .call(xAxis);

            svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

            // Save it off so we can access it later if need be
            tw2.store[selector] = {
                svg: svg,
                data: data,
            };
        });
    }
});
