var showTime=() => {
    let hour = document.getElementById('hour');
    let minute = document.getElementById('minute');
    let second = document.getElementById('second');

    let hh = new Date().getHours();
    let mm = new Date().getMinutes();
    let ss = new Date().getSeconds();

    let doubleNum = (num) => {
        num = num <10 ? "0"+num:num;
        return num;
    }

    hh = doubleNum(hh)
    mm = doubleNum(mm)
    ss = doubleNum(ss)

    hour.innerHTML = hh;
    minute.innerHTML = mm;
    second.innerHTML = ss;

}

setInterval(showTime,1000);
