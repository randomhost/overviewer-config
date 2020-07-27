$(document).ready(function () {

    const screenshotModal = $('#screenshotModal');
    const carouselDom = screenshotModal.find('#carousel-template');
    const carouselIndicatorDom = screenshotModal.find('#carousel-indicator-template');
    const carouselTemplate = carouselDom.clone();
    const carouselIndicatorTemplate = carouselIndicatorDom.clone();

    carouselDom.remove();
    carouselIndicatorDom.remove();

    carouselTemplate.removeAttr('id');
    carouselIndicatorTemplate.removeAttr('id');

    // Sort stats by key
    function sortStats(unordered)
    {
        const ordered = {};
        Object.keys(unordered).sort().forEach(function (key) {
            ordered[key] = unordered[key];
        });

        return ordered;
    }

    // Screenshot Modal
    screenshotModal.on('show.bs.modal', function (event) {
        let link = $(event.relatedTarget);
        let activeImage = link.data('image');
        let images = link.data('images');
        let icon = link.data('icon');
        let title = link.data('title');
        let description = link.data('description');
        let modal = $(this);

        modal.find('#screenshot-title').text(title);
        modal.find('#screenshot-icon').attr('src', icon);
        modal.find('#screenshot-description').text(description);

        let carouselContainer = modal.find('#screenshotCarouselControls .carousel-inner');
        let carouselIndicatorContainer = modal.find('#screenshotCarouselControls .carousel-indicators');

        carouselContainer.empty();
        carouselIndicatorContainer.empty();

        for (let image in images) {
            if (images.hasOwnProperty(image)) {
                let carouselItem = carouselTemplate.clone();
                let carouselIndicatorItem = carouselIndicatorTemplate.clone();

                carouselItem.find('img.screenshot-image').attr('src', 'images/screenshots/' + images[image])
                if (images[image] === activeImage) {
                    carouselItem.addClass('active');
                    carouselIndicatorItem.addClass('active');
                }
                carouselIndicatorItem.attr('data-slide-to', image);

                carouselContainer.append(carouselItem);
                carouselIndicatorContainer.append(carouselIndicatorItem);
            }
        }
    })

    // Stats Modal
    $('#statsModal').on('show.bs.modal', function (event) {
        let link = $(event.relatedTarget);
        let icon = link.data('icon');
        let title = link.data('title');
        let stats = link.data('stats');
        let modal = $(this);

        modal.find('#stats-title').text(title);
        modal.find('#stats-icon').attr('src', icon);

        // General Stats
        let generalHeader = '';
        generalHeader += '<tr>';
        generalHeader += '<th class="col-md-7">Aktion</th>';
        generalHeader += '<th class="col-md-5 text-right">Wert</th>';
        generalHeader += "</tr>\n";
        modal.find('#stats-general table thead').html(generalHeader);

        let generalBody = '';
        for (let stat in sortStats(stats['general']['actions'])) {
            if (stats['general']['actions'].hasOwnProperty(stat)) {
                generalBody += '<tr>';
                generalBody += '<td>' + stats['general']['actions'][stat]['name'] + '</td>';
                generalBody += '<td class="text-right">' + stats['general']['actions'][stat]['value'] + '</td>';
                generalBody += "</tr>\n";
            }
        }
        modal.find('#stats-general table tbody').html(generalBody);

        // Item Stats
        let itemsHeader = '';
        itemsHeader += '<tr>';
        itemsHeader += '<th class="col-md-2">Gegenstand</th>';
        itemsHeader += '<th class="col-md-1 text-center">' + stats['items']['actions']['mined'] + '</th>';
        itemsHeader += '<th class="col-md-1 text-center">' + stats['items']['actions']['broken'] + '</th>';
        itemsHeader += '<th class="col-md-1 text-center">' + stats['items']['actions']['crafted'] + '</th>';
        itemsHeader += '<th class="col-md-1 text-center">' + stats['items']['actions']['used'] + '</th>';
        itemsHeader += '<th class="col-md-1 text-center">' + stats['items']['actions']['picked_up'] + '</th>';
        itemsHeader += '<th class="col-md-1 text-center">' + stats['items']['actions']['dropped'] + '</th>';
        itemsHeader += '</tr>';
        modal.find('#stats-items table thead').html(itemsHeader);

        let itemsBody = '';
        for (let item in sortStats(stats['items']['items'])) {
            if (stats['items']['items'].hasOwnProperty(item)) {
                itemsBody += '<tr>';
                itemsBody += '<td>' + stats['items']['items'][item]['name'] + '</td>';
                itemsBody += '<td class="text-center">' + stats['items']['items'][item]['actions']['mined'] + '</td>';
                itemsBody += '<td class="text-center">' + stats['items']['items'][item]['actions']['broken'] + '</td>';
                itemsBody += '<td class="text-center">' + stats['items']['items'][item]['actions']['crafted'] + '</td>';
                itemsBody += '<td class="text-center">' + stats['items']['items'][item]['actions']['used'] + '</td>';
                itemsBody += '<td class="text-center">' + stats['items']['items'][item]['actions']['picked_up']
                    + '</td>';
                itemsBody += '<td class="text-center">' + stats['items']['items'][item]['actions']['dropped'] + '</td>';
                itemsBody += '</tr>';
            }
        }
        modal.find('#stats-items table tbody').html(itemsBody);

        // Mob Stats
        let mobsHeader = '';
        mobsHeader += '<tr>';
        mobsHeader += '<th class="col-md-4">Kreatur</th>';
        mobsHeader += '<th class="col-md-2 text-center">' + stats['mobs']['actions']['killed'] + '</th>';
        mobsHeader += '<th class="col-md-2 text-center">' + stats['mobs']['actions']['killed_by'] + '</th>';
        mobsHeader += "</tr>\n";
        modal.find('#stats-mobs table thead').html(mobsHeader);

        let mobsBody = '';
        for (let mob in sortStats(stats['mobs']['mobs'])) {
            if (stats['mobs']['mobs'].hasOwnProperty(mob)) {
                mobsBody += '<tr>';
                mobsBody += '<td>' + stats['mobs']['mobs'][mob]['name'] + '</td>';
                mobsBody += '<td class="text-center">' + stats['mobs']['mobs'][mob]['actions']['killed'] + '</td>';
                mobsBody += '<td class="text-center">' + stats['mobs']['mobs'][mob]['actions']['killed_by'] + '</td>';
                mobsBody += '</tr>';
            }
        }
        modal.find('#stats-mobs table tbody').html(mobsBody);
    })
});
