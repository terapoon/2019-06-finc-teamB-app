const express = require('express');
const bcrypt = require('bcrypt');
const jsonwebtoken = require('jsonwebtoken');
const moment = require('moment-timezone');
const multer = require('multer');

const knex = require('./knex');

const jwtToken = 'hogehoge';

const router = express.Router();

// ヘッダに載せられたトークンをもとにユーザーを判別して
// res.locals.idにユーザーidを格納する
router.use((req, res, next) => (async () => {
  try {
    const token = req.get('X-AUTH-TOKEN');
    res.locals.id = jsonwebtoken.verify(token, jwtToken).id;
  } catch (err) {
    res.locals.id = null;
  }

  next();
})());


router.post('/image', multer({ dest: './uploads/' }).single('profile'), (req, res) => {
  res.send({
    filename: req.file.filename,
  });
});

// 指定可能な地域
// [ { id: 1, name: '目黒区' }, ...]
router.get('/areas', (req, res, next) => (async () => {
  const areas = await knex('areas');
  res.send(areas);
})().catch(next));

// 指定可能な時間帯
// [ { id: 1, name: '6:00' }, ...]
router.get('/slots', (req, res, next) => (async () => {
  const slots = await knex('slots');
  res.send(slots);
})().catch(next));

// ユーザー登録
router.post('/register', (req, res, next) => (async () => {
  const {
    email,
    password,
    filename,
    gender,
    name,
    introduction,
    hobbies,
  } = req.body;

  const hashedPassword = await bcrypt.hash(password, 4);

  const [id] = await knex('users').insert({
    email,
    gender,
    name,
    introduce: introduction,
    hobby: hobbies,
    profile_img: filename,
    hashed_password: hashedPassword,
  });

  const token = jsonwebtoken.sign(JSON.stringify({ id }), jwtToken);

  res.send({ token });
})().catch(next));

// ログイン
router.post('/login', (req, res, next) => (async () => {
  const { email, password } = req.body;

  const user = await knex('users')
    .where('email', email)
    .then(i => i[0]);

  if (!user) {
    res.sendStatus(400);
    return;
  }

  const isCorrectPassword = await bcrypt.compare(password, user.hashed_password);

  if (!isCorrectPassword) {
    res.sendStatus(400);
    return;
  }

  const token = jsonwebtoken.sign({ id: user.id }, jwtToken);
  res.cookie('token', token, { httpOnly: false });
  res.send({ token });
})().catch(next));

// 異性の人の中で特定の日付・エリアに該当する人の数を取得する
router.post('/count', (req, res, next) => (async () => {
  const { id } = res.locals;
  const {
    area,
    year, month, date,
  } = req.body;

  const gender = await knex('users')
    .where('id', id)
    .then(i => i[0].gender);

  const count = await knex('users')
    .where({
      available_area: area,
      available_year: year,
      available_month: month,
      available_date: date,
      gender: 1 - gender, // 異性
    })
    .then(i => i.length);

  res.send({
    count,
  });
})().catch(next));

// 自分の情報を更新する
// 次に空いている日付・エリアなど
router.put('/me', (req, res, next) => (async () => {
  const { id } = res.locals;

  const {
    availableYear,
    availableMonth,
    availableDate,
    availableArea,
    availableSlot,
  } = req.body;

  await knex('users')
    .where('id', id)
    .update({
      available_year: availableYear,
      available_month: availableMonth,
      available_date: availableDate,
      available_area: availableArea,
      available_slot: availableSlot,
    });

  res.sendStatus(200);
})().catch(next));

// 現在の自分の情報を取得する
router.get('/me', (req, res, next) => (async () => {
  const { id } = res.locals;

  const user = await knex('users')
    .where('id', id)
    .then(i => i[0]);

  if (!user) {
    res.sendStatus(404);
    return;
  }

  res.send({
    availableYear: user.available_year,
    availableMonth: user.available_month,
    availableDate: user.available_date,
    availableArea: user.available_area,
    availableSlot: user.available_slot,
    profileImg: user.profile_img,
  });
})().catch(next));

// 現在有効なマッチを取得する
// 存在するなら長さ1のリスト
// 存在しないなら空のリスト
router.get('/matches', (req, res, next) => (async () => {
  const { id } = res.locals;

  if (!id) {
    res.sendStatus(400);
    return;
  }

  const me = await knex('users')
    .where('id', id)
    .then(i => i[0]);

  // TODO: 非効率なので書き直す
  const match = await (async () => {
    const all = await knex('matches')
      .where(me.gender === 0 ? 'user_id_male' : 'user_id_female', id);

    const now = moment().tz('Asia/Tokyo');

    return all.find(m => m.year >= now.year() && m.month >= now.month() + 1 && m.date >= now.date());
  })();

  if (!match) {
    res.send([]);
    return;
  }

  res.send([
    {
      year: match.year,
      month: match.month,
      date: match.date,
      slot: match.slot,
      area: match.area,
      ...await knex('users')
        .innerJoin('slots', 'users.available_slot', 'slots.id')
        .innerJoin('areas', 'users.available_area', 'areas.id')
        .where('users.id', me.gender === 0 ? match.user_id_female : match.user_id_male)
        .select(
          'users.name as name',
          'slots.name as slot',
          'areas.name as area',
          'users.profile_img as profileImg',
        )
        .then(i => i[0]),
    },
  ]);
})().catch(next));

// スワイプ用のカードのリストを取得する
router.get('/cards', (req, res, next) => (async () => {
  const { id } = res.locals;

  const me = await knex('users')
    .where('id', id)
    .select(
      'available_year as availableYear',
      'available_month as availableMonth',
      'available_date as availableDate',
      'available_area as availableArea',
      'available_slot as availableSlot',
      'gender',
    )
    .then(i => i[0]);

  // 自分がスワイプ済みのユーザー
  const swipedUserIds = await knex('likes')
    .where('user_id_from', id)
    .select('user_id_to as to')
    .then(i => i.map(j => j.to));

  // 自分をスワイプ済みのユーザー
  const swipedByUserIds = await knex('likes')
    .where('user_id_to', id)
    .select('user_id_from as from')
    .then(i => i.map(j => j.from));

  const ret = [];

  // 自分のことをいいねしていて、自分がまだスワイプしていない人を追加
  await knex('likes')
    .innerJoin('users', 'likes.user_id_from', 'users.id')
    .where('likes.user_id_to', id)
    .where('likes.type', 'like')
    .whereNot('users.id', id)
    .whereNot('users.gender', me.gender)
    .where('users.available_year', me.availableYear)
    .where('users.available_month', me.availableMonth)
    .where('users.available_date', me.availableDate)
    .where('users.available_area', me.availableArea)
    .where('users.available_slot', me.availableSlot)
    .then(i => i.filter(j => !swipedUserIds.includes(j.id)))
    .then(i => i.forEach(j => ret.push({ ...j, liked: true })));

  // 自分のことをまだスワイプしておらず、自分もスワイプしていない人を追加
  await knex('users')
    .whereNot('id', id)
    .whereNot('gender', me.gender)
    .where('available_year', me.availableYear)
    .where('available_month', me.availableMonth)
    .where('available_date', me.availableDate)
    .where('available_area', me.availableArea)
    .where('available_slot', me.availableSlot)
    .then(i => i.filter(j => !swipedByUserIds.includes(j.id) && !swipedUserIds.includes(j.id)))
    .then(i => i.forEach(j => ret.push({ ...j, liked: false })));

  res.send(ret);
})().catch(next));

// いいねを飛ばす
router.post('/likes', (req, res, next) => (async () => {
  const from = res.locals.id;
  const { to } = req.body;
  // 'like' or 'dislike'
  const { type } = req.body;

  await knex('likes')
    .insert({
      type,
      user_id_from: from,
      user_id_to: to,
    });

  if (type === 'like') {
    const isMatched = await knex('likes')
      .where('type', 'like')
      .where('user_id_from', to)
      .where('user_id_to', from)
      .then(i => i.length > 0);

    if (isMatched) {
      const me = await knex('users')
        .where('id', res.locals.id)
        .then(i => i[0]);

      await knex('matches')
        .insert({
          user_id_male: me.gender === 0 ? me.id : to,
          user_id_female: me.gender === 0 ? to : me.id,
          year: me.available_year,
          month: me.available_month,
          date: me.available_date,
          slot: me.available_slot,
          area: me.available_area,
        });

      res.send({
        matched: true,
      });
    }
  }

  res.send({
    matched: false,
  });
})().catch(next));

// チャットの一覧を取得する
router.get('/chats', (req, res, next) => (async () => {

})().catch(next));

// 個別のチャットの情報を取得する
router.get('/chats/:id', (req, res, next) => (async () => {

})().catch(next));

module.exports = router;
