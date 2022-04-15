const monsterRace = ["Aqua","Beast","Beast-Warrior","Creator-God","Cyberse","Dinosaur","Divine-Beast","Dragon","Fairy","Fiend","Fish","Insect","Machine","Plant","Psychic","Pyro","Reptile","Rock","Sea Serpent","Spellcaster","Thunder","Warrior","Winged Beast"]

const spellRace =["Normal","Field","Equip","Continuous","Quick-Play","Ritual"]

const trapRace = ["Normal","Continuous","Counter"]

const attribute = ["DARK","DIVINE","EARTH","FIRE","LIGHT","WATER","WIND"]

const monsterType =[
    "Effect Monster",
    "Flip Effect Monster",
    "Flip Tuner Effect Monster",
    "Gemini Monster",
    "Normal Monster",
    "Normal Tuner Monster",
    "Pendulum Effect Monster",
    "Pendulum Flip Effect Monster",
    "Pendulum Normal Monster",
    "Pendulum Tuner Effect Monster",
    "Ritual Effect Monster",
    "Ritual Monster",
    "Spirit Monster",
    "Toon Monster",
    "Tuner Monster",
    "Union Effect Monster"]

const extraMonsterType = [
    "Fusion Monster",
    "Pendulum Effect Fusion Monster",
    "Synchro Monster",
    "Synchro Pendulum Effect Monster",
    "Synchro Tuner Monster",
    "XYZ Monster",
    "XYZ Pendulum Effect Monster"]

const $type = $(`#cardType`);
const $monster = $(`.monster`);

// enable/disable filter base on card type
$(`#cardType`).on("click",function(e){
    e.preventDefault();

    let cardType = $type.val();
    if(cardType === "Card Type"){
        $(`#cardRace`).prop("disabled",true);
        $monster.prop("disabled",true);
    }
    else{
        $(`#cardRace`).prop("disabled",false);

        if (cardType === "Monster" || cardType === "Extra Monster"){
            $monster.prop("disabled",false);
            populateMon(cardType);
        }
        else{
            $monster.prop("disabled",true);
        }
    }
    populateRace(cardType);
})

// populate race base on card type
function populateRace(cardType){
    let race = [];
    let $cardRace = $(`#cardRace`);
    $cardRace.empty();
    $cardRace.append($(`<option selected>Card Race</option>`));

    if(cardType === "Monster" || cardType === "Extra Monster"){
        race = monsterRace;
    }
    else if (cardType === "Spell Card"){
        race = spellRace;
    }
    else if (cardType === "Trap Card"){
        race = trapRace;
    }

    for(let r of race){
        let v = r.replaceAll(" ","%20");
        let $option = $(`<option value = ${v} >${r}</option>`);
        $cardRace.append($option);
    }
}

// populate monster type & attribute
function populateMon(cardType){
    let type = [];

    // type
    let $monsterType = $(`#monsterType`);
    $monsterType.empty();
    $monsterType.append($(`<option selected>Monster Type</option>`));

    if(cardType === "Monster"){
        type = monsterType
    }
    else if (cardType === "Extra Monster"){
        type = extraMonsterType
    }

    for (let t of type){
        let v = t.replaceAll(" ","%20");
        let $option = $(`<option value=${v}>${t}</option>`);
        $monsterType.append($option);
    }

    // attrubute
    let $attribute = $(`#attribute`);
    $attribute.empty();
    $attribute.append($(`<option selected>Attribute</option>`));

    for(let a of attribute){
        let v = a.replaceAll(" ","%20");
        let $option = $(`<option value=${v}>${a}</option>`);
        $attribute.append($option);
    }
}

// enable/disable scale option base on monster card type
$(`#monsterType`).on("click",function(e){
    e.preventDefault();
    let cardType = $(`#monsterType`).val();

    if (cardType.includes("Pendulum")){
        $(`#scale`).prop("disabled",false);
    }
    else{
        $(`#scale`).prop("disabled",true);
    }
});

// handle search card
$("#searchForm").on("submit",async function(e){
    e.preventDefault();
    const $cardlist = $(".cardlist");
    $cardlist.empty();
    const cards = await axios.get(`/api/card_search?${$(this).serialize()}`)

    // if error append error message
    if (!(Array.isArray(cards.data))){
        let msg = `
        <div class="bg-danger text-white"> 
            ${cards.data.error}
        </div>`
        $cardlist.append(msg)
    }
    else{
        for (let card of cards.data){
            let NewCard = generateCardHTML(card);
            $cardlist.append(NewCard)
        }
    }
})

// Genrate html for card search results
function generateCardHTML(card){
    let type = `${card.type} | ${card.race}`
    // check if the card is monster card
    if ((card.type != "Spell Card") || (card.type != "Trap Card")){
        // check if the card is pendulum monster card
        if(card.scale){
            type.concat(` | Scale:${card["scale"]}`)
        }
        type.concat(`
             | ${card["attribute"]} | Level:${card["level"]} | ATK:${card["atk"]} | DEF:${card["def"]}
        `)
    }

    return `
    <li id= ${card.id}>
        <div class="row m-1 border rounded">
            <div class="col-3 p-2">
                <img src="${card["card_images"][0]["image_url_small"]}" alt="card image">
            </div>
            <div class="col-9 p-2">
                <h4 class="mt-0">${card.name}</h5>
                <h5 class="${card.type}">
                    ${type}
                </h5>
                <p>
                    ${card.desc}
                </p>
            </div>
        </div>
    </li>
    `
}