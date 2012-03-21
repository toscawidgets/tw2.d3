if ( typeof tw2 == "undefined" ) tw2 = {};
if ( typeof tw2.store == "undefined" ) tw2.store = {};
if ( typeof tw2.d3 == "undefined" ) tw2.d3 = {};

$.extend(tw2.d3, {
    timeseries: {
        init: function (
            selector, data, _width, _height,
            padding, interval, n, duration
            ) {
            $(document).ready(function() {
                tw2.d3.timeseries._init(
                    selector, data, _width, _height,
                    padding, interval, n, duration
                );
            });
        },
        _init: function (
            selector, data, _width, _height,
            padding, interval, n, duration
            ) {
            var now = new Date(Date.now() - duration);
            tw2.store[selector] = {value: 0};

            var margin = {
                top: padding[0],
                right: padding[1],
                bottom: padding[2],
                left: padding[3],
            };
            var width = _width - margin.right;
            var height = _height - margin.top - margin.bottom;

            var x = d3.time.scale()
            .domain([now - (n - 2) * duration, now - duration])
            .range([0, width]);

            var y = d3.scale.linear()
            .range([height, 0]);

            var line = d3.svg.line()
            .interpolate("basis")
            .x(function(d, i) { return x(now - (n - 1 - i) * duration); })
            .y(function(d, i) { return y(d); });

            var svg = d3.select("#" + selector).append("p").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .style("margin-left", -margin.left + "px")
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            svg.append("defs").append("clipPath")
            .attr("id", "clip")
            .append("rect")
            .attr("width", width)
            .attr("height", height);

            var axis = svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(x.axis = d3.svg.axis().scale(x).orient("bottom"));

            var path = svg.append("g")
            .attr("clip-path", "url(#clip)")
            .append("path")
            .data([data])
            .attr("class", "line");

            tick();

            function tick() {
                // update the domains
                now = new Date();
                x.domain([now - (n - 2) * duration, now - duration]);
                y.domain([0, d3.max(data)]);

                // push the accumulated value onto the back, and reset the value
                data.push(Math.min(30, tw2.store[selector].value));
                tw2.store[selector].value = 0;

                // redraw the line
                svg.select(".line")
                .attr("d", line)
                .attr("transform", null);

                // slide the x-axis left
                axis.transition()
                .duration(duration)
                .ease("linear")
                .call(x.axis);

                // slide the line left
                path.transition()
                .duration(duration)
                .ease("linear")
                .attr("transform", "translate(" + x(now - (n - 1) * duration) + ")")
                .each("end", tick);

                // pop the old data point off the front
                data.shift();
            }
        },
    },
});
