const monsterRace = ["Aqua","Beast","Beast-Warrior","Creator-God","Cyberse","Dinosaur","Divine-Beast","Dragon","Fairy","Fiend","Fish","Insect","Machine","Plant","Psychic","Pyro","Reptile","Rock","Sea Serpent","Spellcaster","Thunder","Warrior","Winged Beast"]

const spellRace =["Normal","Field","Equip","Continuous","Quick-Play","Ritual"]

const trapRace = ["Normal","Continuous","Counter"]

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

function selectFilter(evt){
    evt.preventDefault();
    console.log("select");

    let cardType = $type.val();
    if (cardType === ("Monster Card" || "Extra Monster Card")){
        $monster.prop("disabled",false);
    }
    else{
        $monster.prop("disabled",true);
    }
}

$(`#cardType`).on("click",selectFilter)