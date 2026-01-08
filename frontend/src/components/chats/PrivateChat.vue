<template>
    <!-- PRYWATNE -->
    <section class="tabpane" id="tab-private">
        <div class="panel">
            <div class="panel-title">Prywatne wiadomości</div>

            <div class="row">
                <select id="dm-user"></select>
                <button id="dm-refresh" type="button" class="ghost">Odśwież</button>
            </div>

            <div id="dm-messages" class="box"></div>

            <form id="dm-form" class="row">
                <input type="text" id="dm-input" placeholder="Napisz prywatnie..." required />
                <button type="submit">Wyślij</button>
            </form>
        </div>
    </section>
</template>
