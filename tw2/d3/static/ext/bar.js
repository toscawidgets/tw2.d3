
if ( typeof tw2 == "undefined" ) tw2 = {};
if ( typeof tw2.store == "undefined" ) tw2.store = {};
if ( typeof tw2.d3 == "undefined" ) tw2.d3 = {};

$.extend(tw2.d3, {
    filter: function(data) {
        // Generic utility.  Remove elements with 0 value from the list.
        // Equivalent to the following python:
        //     >>> data = [d for d in data if d.value > 0]
        for (var i = 0; i < data.length; i++) {
            if (data[i].value <= 0) {
                data.splice(i, 1);
            }
        }
        return data;
    },
    bar: function (selector, data, width, height, padding, format) {
        $(document).ready(function() {
            var w = width - padding[1] - padding[3];
            var h = height - padding[0] - padding[2];

            var format = d3.format(format);

            var x = d3.scale.linear().range([0, w]);
            var y = d3.scale.ordinal().rangeRoundBands([0, h], .1);

            var xAxis = d3.svg.axis().scale(x).orient("top").tickSize(-h);
            var yAxis = d3.svg.axis().scale(y).orient("left").tickSize(0);

            var svg = d3.select("#" + selector).append("svg")
            .attr("width", w + padding[1] + padding[3])
            .attr("height", h + padding[0] + padding[2])
            .append("g")
            .attr("transform", "translate(" + padding[3] + "," + padding[0] + ")");

            // Parse numbers
            $.each(data, function(i, d) { d.value = +d.value; });

            // Save it off so we can access it later if need be
            tw2.store[selector] = {
                svg: svg,
                data: data,
            };

            //            bar.append("text")
            //            .attr("class", "value")
            //            .attr("x", function(d) { return x(d.value); })
            //            .attr("y", y.rangeBand() / 2)
            //            .attr("dx", -3)
            //            .attr("dy", ".35em")
            //            .attr("text-anchor", "end")
            //            .text(function(d) { return format(d.value); });

            svg.append("g").attr("class", "x axis")
            svg.append("g").attr("class", "y axis")

            setInterval(function() {
                tw2.store[selector].data[0].value -= 15;
                tw2.store[selector].data = tw2.d3.filter(tw2.store[selector].data);
                console.log(tw2.store[selector].data);

                var x = d3.scale.linear().range([0, w]);
                var y = d3.scale.ordinal().rangeRoundBands([0, h], .1);

                var xAxis = d3.svg.axis().scale(x).orient("top").tickSize(-h);
                var yAxis = d3.svg.axis().scale(y).orient("left").tickSize(0);

                // Set the scale domain.
                x.domain([0, d3.max(data, function(d) { return d.value; })]);
                y.domain($.map(data, function(d, i) { return d.key; }));

                var bar = svg.selectAll("g.bar").data(
                    tw2.store[selector].data,
                    function(d) { return d.key }
                );

                bar.enter().append("g")
                .attr("class", "bar")
                .append("rect");

                bar.exit().remove();

                bar.transition().duration(750).attr("transform", function(d) {
                    return "translate(0," + y(d.key) + ")";
                });

                bar.selectAll("rect").data(data, function(d) { return d.key })
                .attr("height", y.rangeBand())
                .transition()
                .attr("width", function(d) { return x(d.value); });

                svg.selectAll("g.x").transition().duration(750).call(xAxis);
                svg.selectAll("g.y").transition().duration(750).call(yAxis);

            }, 1000);
        });
    }
});
