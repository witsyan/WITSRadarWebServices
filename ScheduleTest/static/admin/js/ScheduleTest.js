var context = document.getElementById('canvas').getContext('2d');
//document.getElementById('canvas').height = getHseight();
//project 边颜色
//polygonStrokeStyles = [ 'white', 'black'],
polygonStrokeStyles = 'white',
//ScheduleTest 颜色
polygonSStrokeStyles = ['#5ED1D1', '#CE646E'],
//project 颜色
polygonFillStyles = ['rgba(167,142,215,1)', 'rgba(255,196,150,1)'],
//project 图形
shapes = [],
//ScheduleTest 图形 
shapesm = [],
//所有文字
Texts = [],
//把 ScheduleTest 和 project 关联起来
sindex = [],
//表格竖线位置
tline = [198, 398, 598, 799, 1000, 1201, ],
//project x 开始点
xstart = [1, 200, 400, 600, 801, 1002, 1203, ],
//project x 结束点
xend = [195, 395, 595, 796, 997, 1198, 1397, ],
//竖线位置
tline = [198, 398, 598, 799, 1000, 1201, ],
//ScheduleTest x 开始点
xxstart = [4, 202, 402, 602, 803, 1004, 1205, ],
//psend = [191, 196, 196, 196, 196, 196, 196,],
//ScheduleTest x 结束点
xxend = [194, 394, 594, 795, 996, 1197, 1394, ],
//y 开始点
ystart = 4,
//psend = [195, 196, 196, 196, 196, 196, 196,],
//默认行高度
dh = 20,
//projects = [[[开始日期(0~6), 结束日期(0~6), 带几行, "project 名",], [开始日期(0~6), 结束日期(0~6), 第几行, 'ScheduleTest 名,', '完成百分比',]]];
/*projects = [
   [
      [0, 6, 13, "OS X 10.10.2OS X 10.10.2OS X 10.10.2OS X 10.10.2", ],
      [0, 0, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [1, 1, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [2, 2, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [3, 3, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [4, 4, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [5, 5, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [6, 6, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [0, 1, 1, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '1%', ],
      [0, 2, 2, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '11%', ],
      [0, 3, 3, 'sfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdf', '88%', ],
      [0, 4, 4, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [0, 5, 5, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '22%', ],
      [0, 6, 6, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '33%', ],
      [1, 6, 7, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '44%', ],
      [2, 6, 8, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '55%', ],
      [3, 6, 9, 'sfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdf', '99%', ],
      [4, 6, 10, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [5, 6, 11, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '66%', ],
      [6, 6, 12, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '77%', ],
   ],
   [
      [0, 6, 13, "OS X 10.10.2OS X 10.10.2OS X 10.10.2OS X 10.10.2", ],
      [0, 0, 0, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [0, 1, 1, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '1%', ],
      [0, 2, 2, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '11%', ],
      [0, 3, 3, 'sfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdf', '88%', ],
      [0, 4, 4, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [0, 5, 5, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '22%', ],
      [0, 6, 6, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '33%', ],
      [1, 6, 7, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '44%', ],
      [2, 6, 8, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '55%', ],
      [3, 6, 9, 'sfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdfsfsdfsadfdsfsdfsdfsdfsdfsdf', '99%', ],
      [4, 6, 10, '1234567890qwertyuiopasdfghjklzxvbnm,', '100%', ],
      [5, 6, 11, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '66%', ],
      [6, 6, 12, 'sfsdfsadfdsfsdfsdfsdfsdfsdf', '77%', ],
   ],
],*/
//project 名 颜色
projecttextcolor = 'black',
//project 名 字体
projecttextfont = '10pt Helvetica-bold',
//ScheduleTest 名 颜色
ScheduleTesttextcolor = 'white',
//ScheduleTest 名 字体
ScheduleTesttextfont = '9pt Helvetica-bold';

//坐标转换

function windowToCanvas(e) {
   var x = e.x || e.clientX,
      y = e.y || e.clientY,
      bbox = canvas.getBoundingClientRect();

   return {
      x: x - bbox.left * (canvas.width / bbox.width),
      y: y - bbox.top * (canvas.height / bbox.height)
   };
};

//响应点击 onmousedown
//ondblclick
canvas.onclick = function(e) {
   var loc = windowToCanvas(e);
   inshapesm = false
   //alert(loc.x);
   //检测小
   i = 0
   shapesm.forEach(function(polygon) {
      polygon.createPath(context);
      if (context.isPointInPath(loc.x, loc.y)) {
         alert(sindex[i][1] + ' -- ' + sindex[i][0] + ' x:' + loc.x + ' y:' + loc.y);
         //document.getElementById('iframe_a').src = "t2.html";
         document.getElementById('iframe_a').src = "/ScheduleTestselect/?project=" + sindex[i][1] + "&schedule=" + sindex[i][0] + "&id=" + sindex[i][2];
         alert(document.getElementById('iframe_a').src);
         inshapesm = true
      }
      i = i + 1
   });
   /*
   if (!inshapesm) {
      //不在小的里面,检测大的
      i = 0
      shapes.forEach(function(polygon) {
         polygon.createPath(context);
         if (context.isPointInPath(loc.x, loc.y)) {
            alert(projects[i][0][3] + ' x:' + loc.x + ' y:' + loc.y);
            document.getElementById('iframe_a').src = "/ScheduleTestselect/?=xxx";
            //document.getElementById('iframe_a').src = "t2.html";
            alert(document.getElementById('iframe_a').src);
         }
         i = i + 1
      });
   }*/
}

//处理 projects

function projectsinit() {
   for (var i = 0; i < projects.length; ++i) {
      var polygon = new Polygon();
      //起点
      var x = xstart[projects[i][0][0]];
      //长度
      var w = xend[projects[i][0][1]] - x;
      //根据行数计算高度
      var h = projects[i][0][2] * (dh + 5) + 20;
      //文字
      var t = projects[i][0][3];

      var y = ystart;

      polygon.strokeStyle = polygonStrokeStyles;
      //polygon.strokeStyle = polygonStrokeStyles[0];
      //polygonStrokeStyles = polygonStrokeStyles.reverse();
      polygon.fillStyle = polygonFillStyles[0];
      polygonFillStyles = polygonFillStyles.reverse();

      points = [new Point(x, y), new Point(x, y + h), new Point(x + w, y + h), new Point(x + w, y)]
      points.forEach(function(point) {
         polygon.addPoint(point.x, point.y);
      });
      shapes.push(polygon);

      //文字
      var tw = getBtextpxwidth(t, w);
      var text = [tw[0], x + 4, y + 13, tw[1], projecttextcolor, projecttextfont];
      Texts.push(text);
      //fbtext(t, x, y, w);
      //画小个的
      for (var j = 1; j < projects[i].length; ++j) {
         var polygon = new Polygon();
         var xx = xxstart[projects[i][j][0]];
         var yy = ystart + projects[i][j][2] * (dh + 5) + 20;
         var ww = xxend[projects[i][j][1]] - xx;
         var hh = dh;
         var tt = projects[i][j][3];
         var bt = projects[i][j][4];
         polygon.strokeStyle = 'black';
         polygon.fillStyle = polygonSStrokeStyles[0];
         polygonSStrokeStyles = polygonSStrokeStyles.reverse();
         points = [new Point(xx, yy), new Point(xx, yy + hh), new Point(xx + ww, yy + hh), new Point(xx + ww, yy)]
         points.forEach(function(point) {
            polygon.addPoint(point.x, point.y);
         });
         shapesm.push(polygon);
         sindex.push([projects[i][j][3], projects[i][0][3], projects[i][0][4],])

         //文字
         var tw = getSHtextpxwidth(tt, bt, ww);
         var text = [tw[0], xx + 4, yy + 14, tw[1], ScheduleTesttextcolor, ScheduleTesttextfont];
         Texts.push(text);
         //百分比
         var ttw = getSBtextpxwidth(bt, xx, ww);
         var ttext = [bt, ttw[0], yy + 14, ttw[1], ScheduleTesttextcolor, ScheduleTesttextfont];
         Texts.push(ttext);
      }
      //计算下一个 ystart
      ystart = ystart + h + 4;
   }
}


//计算出总高度

function getHseight() {
   var Height = 0;
   for (var i = 0; i < projects.length; ++i) {
      var h = projects[i][0][2] * (dh + 5) + 20;
      Height = Height + h;
   }
   return Height + projects.length * 4 + 4;
}

//获取大文本实际显示文本 文本像素长度(过长的截掉加上 ...)

function getBtextpxwidth(text, w) {
   rtext = ""
   rw = 0
   for (var i = text.length; i > 0; --i) {
      rtext = text.slice(0, i)
      rw = context.measureText(rtext).width;
      if (w - 8 >= rw) {
         //alert(text.slice(0, i));
         break;
      }
   }
   if (text != rtext) {
      rtext = rtext.slice(0, rtext.length - 2) + '...'
   }
   return [rtext, rw]
}

//获取小文本 Head 实际显示文本 文本像素长度(过长的截掉加上 ...)

function getSHtextpxwidth(text, btext, w) {
   rtext = ""
   rw = 0
   for (var i = text.length; i > 0; --i) {
      rtext = text.slice(0, i)
      rw = context.measureText(rtext).width;
      bw = context.measureText(btext).width;
      if (w - bw - 12 >= rw) {
         //alert(text.slice(0, i));
         break;
      }
   }
   if (text != rtext) {
      rtext = rtext.slice(0, rtext.length - 2) + '...'
   }
   return [rtext, rw]
}

//获取百分比位置

function getSBtextpxwidth(text, x, w) {
   var tw = context.measureText(text).width;
   return [w + x - tw - 4, tw]
}

function drawShapes() {
   shapes.forEach(function(shape) {
      shape.stroke(context);
      shape.fill(context);
   });
}

function drawShapesm() {
   shapesm.forEach(function(shapem) {
      shapem.stroke(context);
      shapem.fill(context);
   });
}

//画文字

function drawTexts() {
   Texts.forEach(function(texts) {
      context.save();
      context.fillStyle = texts[4];
      context.font = texts[5];
      context.fillText(texts[0], texts[1], texts[2], texts[3]);
      context.restore();
   });
}

//画竖线

function drawlines() {
   context.beginPath();
   for (var i = 0; i < tline.length; ++i) {
      context.save();
      context.strokeStyle = 'white';
      //context.fillStyle = fillStyle;
      context.moveTo(tline[i], 0);
      context.lineTo(tline[i], getHseight());
      context.stroke();
      context.restore();
   }
}

projectsinit();
drawShapes();
drawShapesm();
drawlines();
drawTexts();