
if ( typeof tw2 == "undefined" ) tw2 = {};
if ( typeof tw2.store == "undefined" ) tw2.store = {};
if ( typeof tw2.d3 == "undefined" ) tw2.d3 = {};

$.extend(tw2.d3, {
    util: {
        filter: function(data) {
            // Generic utility.  Remove elements with 0 value from the list.
            // Equivalent to the following python:
            //     >>> data = [d for d in data if d.value > epsilon]
            var epsilon = 0.001; 
            for (var i = 0; i < data.length; i++) {
                if (data[i].value <= epsilon) {
                    data.splice(i, 1);
                }
            }
            return data;
        },
    },
    bar: {
        init: function (selector, data, width, height, padding, interval) {
            $(document).ready(function() {
                tw2.d3.bar._init(selector, data, width, height, padding, interval);
            });
        },
        _init: function (selector, data, width, height, padding, interval) {
            var w = width - padding[1] - padding[3];
            var h = height - padding[0] - padding[2];

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
                width: width,
                height: height,
                padding: padding,
                interval: interval,
            };

            svg.append("g").attr("class", "x axis")
            svg.append("g").attr("class", "y axis")

            tw2.d3.bar.redraw(selector, 'cubic-in-out')
            if (interval > 0) {
                setInterval(function() {tw2.d3.bar.redraw(selector)}, interval);
            }
        },
        redraw: function(selector, easing) {
            if (typeof easing === 'undefined') { easing = 'linear'; }

            tw2.store[selector].data[0].value -= 15;
            tw2.store[selector].data = tw2.d3.util.filter(
                tw2.store[selector].data
            );
            var data = tw2.store[selector].data;
            var interval = tw2.store[selector].interval;

            var w =
            tw2.store[selector].width - 
            tw2.store[selector].padding[1] -
            tw2.store[selector].padding[3];

            var h =
            tw2.store[selector].height -
            tw2.store[selector].padding[0] -
            tw2.store[selector].padding[2];

            var x = d3.scale.linear().range([0, w]);
            var y = d3.scale.ordinal().rangeRoundBands([0, h], .1);

            var xAxis = d3.svg.axis().scale(x).orient("top").tickSize(-h);
            var yAxis = d3.svg.axis().scale(y).orient("left").tickSize(0);

            // Set the scale domain.
            x.domain([0, d3.max(data, function(d) { return d.value; })]);
            y.domain($.map(data, function(d, i) { return d.key; }));

            var bar = tw2.store[selector].svg.selectAll("g.bar").data(
                data,
                function(d) { return d.key }
            );

            bar.enter().append("g")
            .attr("class", "bar")
            .append("rect");

            bar.exit().remove();

            bar.transition().duration(interval).attr("transform", function(d) {
                return "translate(0," + y(d.key) + ")";
            });

            bar.selectAll("rect")
            .data(data, function(d) { return d.key })
            .attr("height", y.rangeBand())
            .transition().ease(easing).duration(interval)
            .attr("width", function(d) { return x(d.value); });

            tw2.store[selector].svg.selectAll("g.x")
            .transition().ease(easing).duration(interval).call(xAxis);
            tw2.store[selector].svg.selectAll("g.y")
            .transition().ease(easing).duration(interval).call(yAxis);
        },
    },
});
