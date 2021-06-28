from typing import Tuple

import jax.numpy as jnp

from jaxrl.datasets import Batch
from jaxrl.networks.common import InfoDict, Model, Params


def log_prob_update(actor: Model, batch: Batch) -> Tuple[Model, InfoDict]:
    def loss_fn(actor_params: Params) -> Tuple[jnp.ndarray, InfoDict]:
        dist = actor.apply({'params': actor_params}, batch.observations)
        log_probs = dist.log_prob(batch.actions)
        actor_loss = -log_probs.mean()
        return actor_loss, {'actor_loss': actor_loss}

    return actor.apply_gradient(loss_fn)


def mse_update(actor: Model, batch: Batch) -> Tuple[Model, InfoDict]:
    def loss_fn(actor_params: Params) -> Tuple[jnp.ndarray, InfoDict]:
        actions = actor.apply({'params': actor_params}, batch.observations)
        actor_loss = ((actions - batch.actions)**2).mean()
        return actor_loss, {'actor_loss': actor_loss}

    return actor.apply_gradient(loss_fn)