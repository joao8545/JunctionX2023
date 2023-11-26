var currentDate = "2023-11-24";
var currentDay = parseInt(currentDate.split('-')[2]);

var maxDays = 0;
var currentPath = window.location.pathname;
var machine = currentPath.replace("/machines/","");

document.addEventListener('DOMContentLoaded', function() {
    // Fetch the maximum number of days
    fetch('/api/max_days')
        .then(response => response.json())
        .then(data => {
            maxDays = data.max_days;
            updateTimelineData();
        })
        .catch(error => console.error('Error:', error));
});

function changeDay(delta) {
    currentDay += delta;
    if (currentDay <= 23) {
        currentDay = maxDays - 1;
    } else if (currentDay > maxDays) {
        currentDay = 24;
    }
    document.getElementById('currentDay').innerText = 'Day ' + (currentDay);
    currentDate = "2023-11-"+currentDay
    updateTimelineData();
}

function updateTimelineData() {
    fetch('/check_day?machine=' + machine +"&day=" + currentDate)
        .then(response => response.json())
        .then(data => 
            {
                console.log(currentDay);
                console.log(data);
                updateTimelineHTML(data[currentDate]);
            })
        .catch(error => console.error('Error:', error));
}

function updateTimelineHTML(data) {
    console.log(data)
    var timelineContainer = document.getElementById('timelineContent');
    timelineContainer.innerHTML = '';

    for (var hour_data of data) {
        
        var hourContainer = document.createElement('div');
        hourContainer.className = 'hour-container';

        var timeLabel = document.createElement('div');
        timeLabel.className = 'time-label';
        timeLabel.innerText = hour_data.label;

        hourContainer.appendChild(timeLabel);

        for (var bar_data of hour_data.bars) {
            var bar = document.createElement('a');
            bar.className = 'bar';
            bar.setAttribute('data-status', bar_data.status);

            var barInterval = document.createElement('div');
            barInterval.className = 'bar-interval';
            barInterval.innerText = bar_data.label;

            var barTime = document.createElement('div');
            barTime.className = 'bar-time';
            barTime.innerText = bar_data.start;

            bar.appendChild(barInterval);
            bar.appendChild(barTime);

            hourContainer.appendChild(bar);
        }

        timelineContainer.appendChild(hourContainer);
    }
}