if ( typeof tw2 == "undefined" ) tw2 = {};
if ( typeof tw2.store == "undefined" ) tw2.store = {};
if ( typeof tw2.d3 == "undefined" ) tw2.d3 = {};

$.extend(tw2.d3, {
    chord: {
        groupTicks: function(d) {
          /** Returns an array of tick angles and labels, given a group. */
          var k = (d.endAngle - d.startAngle) / d.value;
          return d3.range(0, d.value, 1000).map(function(v, i) {
            return {
              angle: v * k + d.startAngle,
              label: i % 5 ? null : v / 1000 + "k"
            };
          });
        },
        fade: function(opacity, svg) {
            /** Returns an event handler for fading a given chord group. */
            return function(g, i) {
                svg.selectAll("g.chord path")
                .filter(function(d) {
                    return d.source.index != i && d.target.index != i;
                })
                .transition()
            .style("opacity", opacity);
            }
        },
        init: function (selector, data, width, height, padding, colors, interval) {
            $(document).ready(function() {
                tw2.d3.chord._init(selector, data, width/2, height/2, padding, colors, interval);
            });
        },
        _init: function (selector, data, width, height, padding, colors, radial_padding, interval) {
            var w = width - padding[1] - padding[3];
            var h = height - padding[0] - padding[2];

            var chord = d3.layout.chord()
            .padding(radial_padding)
            .sortSubgroups(d3.descending)
            .matrix(data);

            var fill = d3.scale.ordinal()
            .domain(d3.range(data.length))
            .range(colors);

            var svg = d3.select("#" + selector).append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + width/2 + "," + height/2 + ")");

            // Parse numbers
            $.each(data, function(i, row) {
                $.each(row, function(i, entry) {
                    return +entry;
                });
            });

            // Save it off so we can access it later if need be
            tw2.store[selector] = {
                chord: chord,
                svg: svg,
                data: data,
                width: width,
                height: height,
                padding: padding,
                colors: colors,
                interval: interval,
                fill: fill,
            };

            tw2.d3.chord.redraw(selector, 'cubic-in-out')
            if (interval > 0) {
                setInterval(function() {tw2.d3.chord.redraw(selector)}, interval);
            }
        },
        redraw: function(selector, easing) {
            if (typeof easing === 'undefined') { easing = 'linear'; }

            //var data = tw2.store[selector].data;
            var interval = tw2.store[selector].interval;

            var w =
            tw2.store[selector].width - 
            tw2.store[selector].padding[1] -
            tw2.store[selector].padding[3];

            var h =
            tw2.store[selector].height -
            tw2.store[selector].padding[0] -
            tw2.store[selector].padding[2];

            var innerRadius = Math.min(w, h) * .41;
            var outerRadius = innerRadius * 1.1;

            var chord = tw2.store[selector].chord;
            var svg = tw2.store[selector].svg;
            var fill = tw2.store[selector].fill;

            svg.append("g")
            .selectAll("path")
            .data(chord.groups)
            .enter().append("path")
            .style("fill", function(d) { return fill(d.index); })
            .style("stroke", function(d) { return fill(d.index); })
            .attr("d", d3.svg.arc().innerRadius(innerRadius).outerRadius(outerRadius))
            .on("mouseover", tw2.d3.chord.fade(.1, svg))
            .on("mouseout", tw2.d3.chord.fade(1, svg));

            var ticks = svg.append("g")
              .selectAll("g")
                .data(chord.groups)
              .enter().append("g")
              .selectAll("g")
                .data(tw2.d3.chord.groupTicks)
              .enter().append("g")
                .attr("transform", function(d) {
                  return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
                      + "translate(" + outerRadius + ",0)";
                });
            
            ticks.append("line")
                .attr("x1", 1)
                .attr("y1", 0)
                .attr("x2", 5)
                .attr("y2", 0)
                .style("stroke", "#000");
            
            ticks.append("text")
                .attr("x", 8)
                .attr("dy", ".35em")
                .attr("text-anchor", function(d) {
                  return d.angle > Math.PI ? "end" : null;
                })
                .attr("transform", function(d) {
                  return d.angle > Math.PI ? "rotate(180)translate(-16)" : null;
                }).text(function(d) { return d.label; });


            svg.append("g")
            .attr("class", "chord")
            .selectAll("path")
            .data(chord.chords)
            .enter().append("path")
            .style("fill", function(d) { return fill(d.target.index); })
            .attr("d", d3.svg.chord().radius(innerRadius))
            .style("opacity", 1);
        },
    },
});
