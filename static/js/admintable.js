var USR1 = "{{conn['1']['usr']}}";
var USR2 = "{{conn['2']['usr']}}";
var USR3 = "{{conn['3']['usr']}}";
var USR4 = "{{conn['4']['usr']}}";
var IP1 = "{{conn['1']['IP']}}";
var IP2 = "{{conn['2']['IP']}}";
var IP3 = "{{conn['3']['IP']}}";
var IP4 = "{{conn['4']['IP']}}";
var TIME1 = "{{usrtimes[0]}}";
var TIME2 = "{{usrtimes[1]}}";
var TIME3 = "{{usrtimes[2]}}";
var TIME4 = "{{usrtimes[3]}}";
var USRCOUNT = "{{conn['connCount']}}";

document.getElementById('USR1').innerHTML = USR1;
document.getElementById('USR2').innerHTML = USR2;
document.getElementById('USR3').innerHTML = USR3;
document.getElementById('USR4').innerHTML = USR4;
document.getElementById('IP1').innerHTML = IP1;
document.getElementById('IP2').innerHTML = IP2;
document.getElementById('IP3').innerHTML = IP3;
document.getElementById('IP4').innerHTML = IP4;
document.getElementById('TIME1').innerHTML = TIME1;
document.getElementById('TIME2').innerHTML = TIME2;
document.getElementById('TIME3').innerHTML = TIME3;
document.getElementById('TIME4').innerHTML = TIME4;

document.getElementById('USRCOUNT').innerHTML = USRCOUNT;
